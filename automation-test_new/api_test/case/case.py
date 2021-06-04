import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.case_write_excel import CaseWrite
from api_test.common.common import record_caseDynamic
from api_test.models import CaseInfo, CaseProject, CaseRequirement, CaseOperationHistory
from api_test.serializers import CaseSerializer, CaseProjectSerializer, CaseDeserializer, CaseOperationHistorySerializer

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CaseList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        caseRequirement_id = request.GET.get("caseRequirement_id")
        # 根据字段获取信息，排除逻辑删除的数据
        if name or caseRequirement_id:
            obi = CaseInfo.objects.filter(name__contains=name, caseProject_id=request.GET.get("caseProject_id"), caseRequirement=caseRequirement_id, yn=0).order_by("-id")
        else:
            obi = CaseInfo.objects.filter(caseProject_id=request.GET.get("caseProject_id"), yn=0).order_by("-id")
        paginator = Paginator(obi, page_size)
        total = paginator.num_pages # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = CaseSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功")


class CaseInformation(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例列表
        :param request:
        :return:
        """
        try:
            if not request.GET.get("id"):
                return JsonResponse(code="999996", msg="参数有误!")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误")
        id = request.GET.get("id")
        obi = CaseInfo.objects.get(id=id, yn=0)
        serialize = CaseSerializer(obi)
        return JsonResponse(data=serialize.data, code="999999", msg="成功")


class AddCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验必传参数
            if not data["caseProject_id"] or not data["name"] or not data["caseRequirement_id"] or not \
                    data["operationSteps"] or not data["priority"] or not data["expectedResults"] or not data["actualResult"]:
                return JsonResponse(code="999996", msg="参数有误!")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误!")

    def post(self, request):
        """
        新增用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["userUpdate"] = request.user.pk
        try:
            obj = CaseProject.objects.get(id=data["caseProject_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在!")
        pro_data = CaseProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        case_name = CaseInfo.objects.filter(name=data["name"], caseProject=data["caseProject_id"], yn=0)
        if len(case_name):
            return JsonResponse(code="999997", msg="存在相同名称!")
        else:
            with transaction.atomic():  # 执行错误后，帮助事物回滚
                serialize = CaseDeserializer(data=data)
                if serialize.is_valid():
                    try:
                        if not isinstance(data.get("caseRequirement_id"), int):
                            return JsonResponse(code="999996", msg="参数有误!")
                        obi = CaseRequirement.objects.get(id=data["caseRequirement_id"], caseProject=data["caseProject_id"])
                        serialize.save(caseProject=obj, caseRequirement=obi)
                    except KeyError:
                        serialize.save(caseProject=obj)
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999991", msg="需求不存在!")
                    case_id = serialize.data.get("id")
                    record_caseDynamic(caseProject=data["caseProject_id"],
                                   _type="新增", operationObject="用例", user=request.user.pk,
                                   data="新增用例“%s”" % data["name"])
                    case_record = CaseOperationHistory(case=CaseInfo.objects.get(id=case_id),
                                                     user=User.objects.get(id=request.user.pk),
                                                     description="新增用例“%s”" % data["name"])
                    case_record.save()
                    return JsonResponse(code="999999", msg="成功!", data={"case_id": case_id})
                return JsonResponse(code="999996", msg="参数有误!")


class UpdateCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验必传参数
            if not data["caseProject_id"]:
                return JsonResponse(code="999996", msg="参数有误!")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误!")

    def post(self, request):
        """
        更新用例
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["userUpdate"] = request.user.pk
        try:
            pro_data = CaseProject.objects.get(id=data["caseProject_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        if data.get("id"):
            try:
                obj = CaseInfo.objects.get(id=data["id"], yn=0)
            except ObjectDoesNotExist:
                return JsonResponse(code="999992", msg="用例不存在！")
            else:
                with transaction.atomic():  # 执行错误后，帮助事物回滚
                    serialize = CaseDeserializer(data=data)
                    if serialize.is_valid():
                        data["userUpdate"] = request.user
                        serialize.update(instance=obj, validated_data=data)
                        record_caseDynamic(caseProject=data["caseProject_id"],
                                           _type="更新", operationObject="用例", user=request.user.pk,
                                           data="更新用例“%s”" % data["name"])
                        case_record = CaseOperationHistory(case=CaseInfo.objects.get(id=data["id"]),
                                                           user=User.objects.get(id=request.user.pk),
                                                           description="更新用例“%s”" % data["name"])
                        case_record.save()
                        return JsonResponse(code="999999", msg="成功!", data={"case_id": data["id"]})
                    return JsonResponse(code="999996", msg="参数有误!")
        else:
            try:
                for i in data["ids"]:
                    try:
                        obj = CaseInfo.objects.filter(id=i, yn=0)
                    except ObjectDoesNotExist:
                        return JsonResponse(code="999992", msg="用例不存在！")
                    else:
                        with transaction.atomic():  # 执行错误后，帮助事物回滚
                            if obj:
                                obj.update(actualResult=data['actualResult'], userUpdate=data["userUpdate"])
                                record_caseDynamic(caseProject=data["caseProject_id"],
                                               _type="更新", operationObject="用例", user=request.user.pk,
                                               data="更新用例“%s”" % obj[0].name)
                                case_record = CaseOperationHistory(case=CaseInfo.objects.get(id=i),
                                                                 user=User.objects.get(id=request.user.pk),
                                                                 description="更新用例“%s”" % obj[0].name)
                                case_record.save()
                            else:
                                return JsonResponse(code="999996", msg="参数有误!")
                return JsonResponse(code="999999", msg="成功!")
            except ObjectDoesNotExist:
                return JsonResponse(code="999996", msg="参数有误!")


class DelCase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["ids"], list):
                for i in data["ids"]:
                    if not isinstance(i, int):
                        return JsonResponse(code="999995", msg="参数有误！")
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        删除需求
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = CaseProject.objects.get(id=data["caseProject_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            for j in data["ids"]:
                obj = CaseInfo.objects.filter(id=j, yn=0)
                if obj:
                    name = obj[0].name
                    obj.update(yn=1)
                    record_caseDynamic(caseProject=data["caseProject_id"],
                                   _type="删除", operationObject="用例", user=request.user.pk, data=name)
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="失败！")


class CaseDynamic(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        接口操作历史
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        caseProject_id = request.GET.get("caseProject_id")
        case_id = request.GET.get("case_id")
        if not caseProject_id or not case_id:
            return JsonResponse(code="999996", msg="参数有误!")
        try:
            pro_data = CaseProject.objects.get(id=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在!")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            CaseInfo.objects.get(id=case_id, caseProject=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="接口不存在!")
        obn = CaseOperationHistory.objects.filter(case=case_id).order_by("-time")
        paginator = Paginator(obn, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = CaseOperationHistorySerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功!")


class CaseExportExcel(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验caseProject_id类型为int
            if not data.GET.get("caseProject_id") or not data.GET.get("caseRequirement_id"):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def get(self, request):
        """
        启用项目
        :param request:
        :return:
        """
        result = self.parameter_check(request)

        if result:
            return result
        obj = CaseRequirement.objects.get(id=request.GET.get("caseRequirement_id"), caseProject_id=request.GET.get("caseProject_id"), yn=0)
        obi = CaseInfo.objects.filter(caseProject_id=request.GET.get("caseProject_id"), caseRequirement=request.GET.get("caseRequirement_id"), yn=0).order_by("id")
        serialize = CaseSerializer(obi, many=True).data
        path = "./api_test/ApiDoc/%s.xlsx" % str(obj.name)
        write_result = CaseWrite(path).case_write_schedule(serialize)
        if write_result:
            return JsonResponse(code="999999", msg="成功！", data=path)
        else:
            return JsonResponse(code="999998", msg="失败")


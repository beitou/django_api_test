import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from api_test.common.api_response import JsonResponse
from api_test.common.common import record_caseDynamic
from api_test.models import CaseRequirement, CaseProject, CaseInfo
from api_test.serializers import CaseRequirementSerializer, CaseRequirementDeserializer, CaseProjectSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CaseRequirementList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取需求列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 10))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        id = request.GET.get("id")
        if name:
            obi = CaseRequirement.objects.filter(name__contains=name, caseProject_id=request.GET.get("caseProject_id"), yn=0).order_by("-id")
        elif id:
            obi = CaseRequirement.objects.filter(id__contains=id, caseProject_id=request.GET.get("caseProject_id"), yn=0).order_by("-id")
        else:
            obi = CaseRequirement.objects.filter(caseProject_id=request.GET.get("caseProject_id"), yn=0).order_by("-id")
        paginator = Paginator(obi, page_size)
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = CaseRequirementSerializer(obm, many=True)
        if serialize.data:
            if serialize.data[0].get('casePassCount') != 0:
                serialize.data[0]['passingRate'] = round(serialize.data[0].get('casePassCount') /
                                                         serialize.data[0].get('caseRequirementCount'), 2)
            else:
                serialize.data[0]['passingRate'] = '0'
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功")


class AddCaseRequiremen(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增需求
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = request.user.pk
        caseRequirement_serializer = CaseRequirementDeserializer(data=data)
        obi = CaseProject.objects.get(id=data['caseProject_id'])
        try:
            CaseRequirement.objects.get(name=data["name"], caseProject=data['caseProject_id'], yn=0)

            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if caseRequirement_serializer.is_valid():
                    # 保存新需求
                    caseRequirement_serializer.save(caseProject=obi)
                    # 记录动态
                    record_caseDynamic(caseProject=caseRequirement_serializer.data.get("id"),
                                       _type="添加", operationObject="需求", user=request.user.pk, data=data["name"])
                    return JsonResponse(data={
                        "caseProject_id": caseRequirement_serializer.data.get("id")
                    }, code="999999", msg="成功")
                else:
                    print(caseRequirement_serializer.errors)
                    return JsonResponse(code="999998", msg="失败")


class DelCaseRequiremen(APIView):
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
            if not isinstance(data["ids"], list) or not isinstance(data["caseProject_id"], int):
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
                obj = CaseRequirement.objects.filter(id=j, yn=0)
                if obj:
                    name = obj[0].name
                    obj.update(yn=1)
                    record_caseDynamic(caseProject=data["caseProject_id"],
                                       _type="删除", operationObject="需求", user=request.user.pk, data=name)
                    obk = CaseInfo.objects.filter(caseRequirement_id=j, yn=0)
                    if len(obk) > 0:
                        obk.update(yn=1)
                        for k in range(len(obk)):
                            name = obk[k].name
                            record_caseDynamic(caseProject=data["caseProject_id"],
                                               _type="删除", operationObject="用例", user=request.user.pk, data=name)
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="失败！")


class UpdateCaseRequiremen(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, host
            if not data["name"]:
                return JsonResponse(code="999995", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999995", msg="参数有误！")

    def post(self, request):
        """
        修改需求
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
            obi = CaseRequirement.objects.get(id=data["id"], yn=0)
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="需求不存在！")
        else:
            serializer = CaseRequirementDeserializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.update(instance=obi, validated_data=data)
                    # 记录动态
                    record_caseDynamic(caseProject=data["caseProject_id"],
                                       _type="修改", operationObject="需求", user=request.user.pk, data=data["name"])
                    return JsonResponse(code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")

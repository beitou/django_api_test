import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.common import record_caseDynamic
from api_test.models import CaseProjectMember, CaseReportSendConfig,CaseProject
from api_test.serializers import CaseProjectMemberSerializer, CaseReportSendConfigSerializer, \
    CaseReportSendConfigDeserializer, CaseProjectSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class ProjectMemberList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目成员列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        caseProject_id = request.GET.get("caseProject_id")

        if not caseProject_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not caseProject_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = CaseProject.objects.get(id=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = CaseProjectMember.objects.filter(caseProject_id=caseProject_id).order_by("id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = CaseProjectMemberSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功！")


class EmailConfig(APIView):
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
            if not isinstance(data["caseProject_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, host
            if not data["reportFrom"] or not data["mailUser"] or not data["mailPass"] :
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        添加或修改邮件发送配置
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obi = CaseProject.objects.get(id=data["caseProject_id"])
            if not request.user.is_superuser and obi.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(obi)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        serialize = CaseReportSendConfigDeserializer(data=data)
        if serialize.is_valid():
            try:
                obj = CaseReportSendConfig.objects.get(caseProject=data["caseProject_id"])
                serialize.update(instance=obj, validated_data=data)
            except ObjectDoesNotExist:
                serialize.save(caseProject=obi)
            # 记录动态
            record_caseDynamic(caseProject=data["caseProject_id"],
                           _type="添加", operationObject="邮箱", user=request.user.pk, data="添加邮箱配置")
            return JsonResponse(code="999999", msg="成功！")
        return JsonResponse(code="999996", msg="参数有误！")


class DelEmail(APIView):
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
            if not isinstance(data["caseProject_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除邮箱配置
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = CaseProject.objects.get(id=data["caseProject_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        CaseReportSendConfig.objects.filter(project=data["caseProject_id"]).delete()
        # 记录动态
        record_caseDynamic(caseProject=data["caseProject_id"],
                       _type="删除", operationObject="邮箱", user=request.user.pk, data="删除邮箱配置")
        return JsonResponse(code="999999", msg="成功！")


class GetEmail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取邮箱配置
        :param request:
        :return:
        """
        caseProject_id = request.GET.get("caseProject_id")
        if not caseProject_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not caseProject_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = CaseProject.objects.get(id=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = CaseProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = CaseReportSendConfig.objects.get(caseProject=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999999", msg="成功！")
        data = CaseReportSendConfigSerializer(obj).data
        return JsonResponse(code="999999", msg="成功！", data=data)


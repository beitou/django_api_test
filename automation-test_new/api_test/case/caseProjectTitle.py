import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.models import CaseProject
from api_test.serializers import CaseProjectSerializer

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CaseProjectInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取用例项目详情
        :param request:
        :return:
        """
        caseProject_id = request.GET.get("caseProject_id")
        if not caseProject_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not caseProject_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        # 查找项目是否存在
        try:
            obj = CaseProject.objects.get(id=caseProject_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        serialize = CaseProjectSerializer(obj)
        if serialize.data["status"]:
            return JsonResponse(data=serialize.data, code="999999", msg="成功！")
        else:
            return JsonResponse(code="999985", msg="该项目已禁用")

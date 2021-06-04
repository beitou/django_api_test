import logging
import requests
from requests import RequestException
from rest_framework.authentication import TokenAuthentication

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.zentao import ZenTao

logger = logging.getLogger( __name__ )  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class RequirementBug(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        try:
            # 校验必传参数
            if not request.GET.get("zentao_id"):
                return JsonResponse(code="999996", msg="参数有误!")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误!")
        try:
            s = requests.session()
            z = ZenTao(s, 'mingxi', 'hlj@123', request.GET.get("zentao_id"))
            z.get_zentaosid()
            bug_count = z.count_bugs()
        except RequestException:
            return JsonResponse(code="999998", msg="蝉道请求失败!")
        return JsonResponse(data=bug_count, code="999999", msg="成功")

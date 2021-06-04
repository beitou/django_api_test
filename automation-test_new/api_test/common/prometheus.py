from rest_framework.views import APIView
from api_test.common.api_response import JsonResponse
from rest_framework.authentication import TokenAuthentication


class Prometheus(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        公司监控默认返回
        :param request:
        :return:
        """
        return JsonResponse(status=200, code=200, msg='success', data=[])


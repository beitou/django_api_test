import logging

import requests
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CustomUrl(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        loginCookie = ''
        urlType = request.GET.get("urlType")
        if urlType == 'sso':
            loginCookie = self.getSSOCookie()
        return JsonResponse(data={"Cookie": loginCookie})

    def getSSOCookie(self):
        s = requests.session()
        # 登录获取token
        address = 'http://admin-sso.stg.xxx.com/sso/login'
        data = {
            'loginName': 'mingxi',
            'password': 'mingxi'
        }
        head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}
        s.post(url=address, data=data, headers=head)
        cookies_value = s.cookies.get_dict()
        loginCookie = 'sso_token=' + cookies_value['sso_token']
        return loginCookie



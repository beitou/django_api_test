import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
import requests
from api_test.common.common import record_caseDynamic
from api_test.models import CaseInfo, CaseProject, CaseRequirement, CaseOperationHistory
from api_test.serializers import CaseSerializer, CaseProjectSerializer, CaseDeserializer

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class Tquest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        authentication_classes = (TokenAuthentication,)
        permission_classes = ()

        print()
        response = requests.get(request.GET.get("url"))
        print(response.json())
        return JsonResponse(data={"data": 'success'}, code="999999", msg="成功")




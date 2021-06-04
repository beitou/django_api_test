import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.models import ScriptGroup
from api_test.serializers import ScriptGroupSerializer, ScriptGroupDeserializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class ScriptGroupList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        脚本类型
        :param request:
        :return:
        """

        try:
            pro_data = ScriptGroup.objects.filter(status='1')
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="请添加脚本分类!")
        # 序列化结果

        serialize = ScriptGroupSerializer(pro_data, many=True)
        return JsonResponse(data=serialize.data, code="999999", msg="成功!")


class AddScriptGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        新增脚本类型
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        # 反序列化
        serializer = ScriptGroupDeserializer(data=data)
        # 校验反序列化正确，正确则保存，外键为project
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(code="999998", msg="失败!")

        return JsonResponse(code="999999", msg="成功!")


class UpdateScriptGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        新增脚本类型
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        # 反序列化
        serializer = ScriptGroupDeserializer(data=data)
        # 校验反序列化正确，正确则保存，外键为project
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(code="999998", msg="失败!")

        return JsonResponse(code="999999", msg="成功!")


class DelScriptGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """
        修改接口分组名称
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        pro_data = ScriptGroup.objects.filter(status='1', name=data['name'])
        if pro_data:
            pro_data.delete()
        else:
            return JsonResponse(code="999991", msg="分类不存在!")

        return JsonResponse(code="999999", msg="成功!")

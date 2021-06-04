import logging

import os
from django.db import transaction

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from api_test.common.api_response import JsonResponse

from api_test.serializers import ScriptFileSerializer, ScriptFileDeserializer
from api_test.models import ScriptFile


class uploadFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        data = request.data
        f = data.get("file")
        fileDetail = ''''''
        for i in f.chunks():
            temp = i.decode(encoding='utf-8')
            fileDetail = fileDetail + temp

        scriptfile = {}
        scriptfile["sid"] = data.get("script_id")
        scriptfile["fileName"] = f.name
        scriptfile["fileDetail"] = fileDetail
        scriptfile["user"] = request.user.pk

        # 需要添加逻辑，验证文件是否存在
        scriptFile = ScriptFile.objects.filter(sid=data.get("script_id"), fileName=f.name)
        if scriptFile:
            scriptFile.update(fileDetail=fileDetail, status="1")
            return JsonResponse(code="999999", msg="上传成功")
        else:
            scriptFileDeserializer = ScriptFileDeserializer(data=scriptfile)
            if scriptFileDeserializer.is_valid():
                scriptFileDeserializer.save()
                return JsonResponse(code="999999", msg="上传成功")
            else:
                return JsonResponse(code="999998", msg="上传失败")

        # data = request.data
        # f = data.get("file")
        #
        # filepath = os.path.dirname(__file__).replace("/api_test/common","")+"/Script/" +f.name
        # f1 = open(filepath, mode='wb')
        # for i in f.chunks():
        #     f1.write(i)
        # f1.close()
        #
        # return JsonResponse(code="999999", msg="成功")
        # except ObjectDoesNotExist:
        #     return JsonResponse(code="999995", msg="项目不存在！")


class deleteFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        # data = JSONParser().parse(request)
        # result = self.parameter_check(data)
        # if result:
        #     return result
        # # 查找项目是否存在
        # try:
        #     obj = CaseProject.objects.get(id=data["caseProject_id"])
        #     if not request.user.is_superuser and obj.user.is_superuser:
        #         return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
        #     obj.status = True
        #     obj.save()
        #     record_caseDynamic(caseProject=data["caseProject_id"],
        #                    _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
        data = request.data
        fileName = data["fileName"]
        script_id = data["script_id"]

        obj = ScriptFile.objects.filter(sid=script_id, fileName=fileName)
        with transaction.atomic():
            obj.update(status="0")

        return JsonResponse(code="999999", msg="成功")


class updateFile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):

        data = request.data

        scriptfile = {}
        scriptfile["sid"] = data.get("script_id")
        scriptfile["fileName"] = data["fileName"]
        scriptfile["fileDetail"] = data["fileDetail"]
        scriptfile["user"] = request.user.pk

        # 需要添加逻辑，验证文件是否存在
        scriptFile = ScriptFile.objects.filter(sid=data.get("script_id"), fileName=data["fileName"])
        if scriptFile:
            scriptFile.update(fileDetail=data["fileDetail"], status="1")
            return JsonResponse(code="999999", msg="上传成功")
        else:
            scriptFileDeserializer = ScriptFileDeserializer(data=scriptfile)
            if scriptFileDeserializer.is_valid():
                scriptFileDeserializer.save()
                return JsonResponse(code="999999", msg="更新成功")
            else:
                return JsonResponse(code="999998", msg="更新失败")


class getFileDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        # data = JSONParser().parse(request)
        # result = self.parameter_check(data)
        # if result:
        #     return result
        # # 查找项目是否存在
        # try:
        #     obj = CaseProject.objects.get(id=data["caseProject_id"])
        #     if not request.user.is_superuser and obj.user.is_superuser:
        #         return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
        #     obj.status = True
        #     obj.save()
        #     record_caseDynamic(caseProject=data["caseProject_id"],
        #                    _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
        fileName = request.GET.get("fileName")
        script_id = request.GET.get("script_id")

        obj = ScriptFile.objects.filter(sid=script_id, fileName=fileName, status='1')
        if obj.count() > 1:
            return JsonResponse(code="999998", msg="数据库有多条相同数据，请处理")
        else:
            obj = obj.first()
            serializer = ScriptFileSerializer(obj)
            return JsonResponse(data={"getFile": serializer.data}, code="999999", msg="成功")

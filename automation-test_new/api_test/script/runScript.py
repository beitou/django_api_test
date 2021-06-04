import logging
import os
import subprocess
import sys

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from api_test.common.api_response import JsonResponse
from api_test.common.warning_message import send_message
from api_test.models import Script, ScriptFile, ScriptParameter

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class RunScript(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """

        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/script_code_dir/"
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        scriptFiles = ScriptFile.objects.filter(sid=data["script_id"], status='1')
        for f1 in scriptFiles:
            filepath = baseDir + f1.fileName
            f = open(filepath, 'w')
            f.write(f1.fileDetail)
            f.close()
        try:
            execFile = ScriptFile.objects.get(sid=data["script_id"], status='1', executable='1')
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="未找到可执行文件！")

        spobj = ScriptParameter.objects.filter(sid=data["script_id"])
        parameters = ''
        mobiles = ""
        for spo in spobj:
            parameters = parameters + "\"" + spo.name + "\":\"" + spo.value + "\","
            mobiles = mobiles + spo.name + ',\n'
        parameters = " '{" + parameters + "}'"
        parameters = parameters.replace(",}", "}")
        #sudo -i
        command = "sudo -i python3 " + baseDir + execFile.fileName + parameters
        print(command)
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = result.stdout.read()
        send_message(request.user.username+'--'+data['name']+" : "+mobiles)
        # result = exec(filepath)
        for f1 in scriptFiles:
            filepath = baseDir + f1.fileName
            os.remove(filepath)
        return JsonResponse(code="999999", msg="成功!", data={"resultCode": result})

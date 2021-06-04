import logging
import os
import subprocess
import sys

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from api_test.common.warning_message import send_message

from api_test.common.api_response import JsonResponse

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class RunCode(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        """

        :param request:
        :return:
        """
        data = JSONParser().parse(request)

        code = data['code']
        scname = data['name']
        paramter = data['parameter']
        # print(paramter)
        baseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/script_code_dir/"
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        filepath = baseDir + "/code.py"
        f = open(filepath, 'w')
        f.write(code)
        f.close()
        parameters = ""
        content = ""
        for p in paramter:
            if p.get("name") != '':
                parameters = parameters + " \"" + p.get("name") + "\":\"" + p.get("value") + "\","
                content = content + '手艺人：' + p.get('description') + '  ' + '手机号：' + p.get("name") + '\n'
        parameters = " '{" + parameters + "}'"
        parameters = parameters.replace(",}", "}")
        command = "sudo -i python3 " + filepath + parameters
        # print(command)
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = result.stdout.read()
        send_message(content + '已经被' + "【" + request.user.username + "】" + scname)
        # result = exec(filepath)
        os.remove(filepath)
        return JsonResponse(code="999999", msg="成功!", data={"resultCode": result})

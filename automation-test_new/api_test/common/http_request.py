import logging


from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from api_test.common.api_response import JsonResponse
import requests
from api_test.common import confighttp
import re
import json
import dubbo_telnet

from api_test.models import GlobalHost

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class httpRequest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        data = JSONParser().parse(request)
        print(data['parameter'])
        url = request.GET.get("url")
        # header = request.
        request_parameter_type = request.GET.get("parameter_type")
        data = request.query_params

        responseCode,responseData,responseHeader = confighttp.get('', url, request_parameter_type, data)
        print("responseHeader",responseHeader)
        return JsonResponse(data={"data": responseData,
                                  "Header": responseHeader,
                                  }, code=responseCode, msg="成功")

    def post(self,request):
        data = JSONParser().parse(request)
        if data['request_type'] == 'DUBBO':
            host_value = GlobalHost.objects.get(id=data["host_id"]).host
            Host, Port = host_value.split(':')
            # 初始化dubbo对象
            conn = dubbo_telnet.connect(Host, Port)

            # 设置telnet连接超时时间
            conn.set_connect_timeout(100)

            # 设置dubbo服务返回响应的编码
            conn.set_encoding('gbk')

            interface = data["url"]

            method = data['dubboMethod']
            common_value_str = ''
            common_value_int = ''

            parameters = data['parameter']
            request_parameter_type = data['parameter_type']
            if request_parameter_type == "form-data":
                if type(parameters) == str:
                    parameters = json.loads(parameters)
                else:
                    temp = {}
                    for i in parameters:
                        temp[i.get("name")] = i.get("value")
                    parameters = temp
            if parameters.get('dubbo-str'):
                common_value_str = parameters.get('dubbo-str')
                for i in common_value_str.split(','):
                    common_value_str = '"' + i + '",'
                del parameters['dubbo-str']
            if parameters.get('dubbo-int'):
                common_value_int = parameters.get('dubbo-int')
                for i in common_value_int.split(','):
                    common_value_int = i + ','
                del parameters['dubbo-int']
            param = json.dumps(parameters)
            param = common_value_str + common_value_int + param
            result = conn.invoke(interface, method, param)
            if result is None:
                return JsonResponse(data={"data": result,
                                          }, code=500, msg="失败")
            else:
                return JsonResponse(data={"data": result,
                                          }, code=200, msg="成功")
        else:
            parameters = data['parameter']
            request_parameter_type = data['parameter_type']
            if request_parameter_type=="form-data":
                if type(parameters)==str :
                    parameters = json.loads(parameters)
                else:
                    temp={}
                    for i in parameters:
                        temp[i.get("name")]=i.get("value")
                    parameters = temp
            # elif request_parameter_type=="raw":
            #     parameters = eval(parameters)
            header = data['headDict']

            host_value = GlobalHost.objects.get(id=data["host_id"]).host

            url = data['protocol'] + "://" + host_value + data['url']
            # data = request.POST.get("data")
            print(request.META.get("HTTP_AUTHORIZATION"))

            request_type = data['request_type']
            request_type = request_type.lower()
            if request_type == "get":
                responseCode, responseData, responseHeader = confighttp.get(header, url, request_parameter_type, parameters)
            else:
                responseCode, responseData, responseHeader = confighttp.post(header, url, request_parameter_type, parameters)
            return JsonResponse(data={"data": responseData,
                                      "Header": responseHeader,
                                      }, code=responseCode, msg="成功")


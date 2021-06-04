import django
import sys
import os
import json
import dubbo_telnet

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_automation_test.settings")
django.setup()

import json
import logging
import re
import operator
import datetime

import requests
import simplejson
from django.core import serializers
from requests import ReadTimeout
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError
from api_test.common.common import check_json, record_results
from api_test.models import GlobalHost, AutomationScheduleApi, AutomationParameter, AutomationTestResult, \
    AutomationHead, \
    AutomationParameterRaw
from api_test.serializers import AutomationScheduleApiSerializer, AutomationParameterRawSerializer
from api_test.common.json_operator import get_json_value

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def test_api(schedule_id, project_id, _id, start_time=datetime.datetime.now(), is_auto=False):
    """
    执行接口测试
    :param host_id: 测试的host域名
    :param schedule_id: 测试计划ID
    :param _id:  计划下接口ID
    :param project_id: 所属项目
    :return:
    """

    data = AutomationScheduleApiSerializer(
        AutomationScheduleApi.objects.get(id=_id, automationTestSchedule=schedule_id)).data
    host = GlobalHost.objects.get(id=data['host_id'], project=project_id)
    http_type = data['httpType']
    request_type = data['requestType']
    if data['apiAddress'].startswith('http'):
        url = data['apiAddress']
    else:
        address = host.host + data['apiAddress']
        if http_type == 'HTTP':
            url = 'http://' + address
        else:
            url = 'https://' + address
    head = json.loads(serializers.serialize('json', AutomationHead.objects.filter(automationScheduleApi=_id)))
    header = {}
    request_parameter_type = data['requestParameterType']
    examine_type = data['examineType']
    http_code = data['httpCode']
    response_parameter_list = data['responseData']
    if data['requestParameterType'] == 'form-data':
        parameter_list = json.loads(serializers.serialize('json',
                                                          AutomationParameter.objects.filter(
                                                              automationScheduleApi=_id)))
        parameter = {}
        parameter_list_data = {}

        for i in parameter_list:
            key_ = i['fields']['name']
            value = i['fields']['value']

            try:
                if value in parameter_list_data:
                    parameter[key_] = parameter_list_data.get(value)
                elif i['fields']['interrelate']:
                    try:
                        param_data = get_special_parameter_value(value, schedule_id, project_id)
                    # value_list = re.findall('(?<=\[).*?(?=])', value)
                    # # 参数类型
                    # interrelate_type = value_list[2]
                    # if interrelate_type == "JSON":
                    #     api_id = value_list[0]
                    #     param = value_list[3]
                    #     try:
                    #         temp = AutomationTestResult.objects.filter(automationScheduleApi=api_id)
                    #         if len(temp) == 0:
                    #             param_data = AutomationScheduleApi.objects.filter(name=api_id,
                    #                                                               automationTestSchedule=schedule_id)
                    #             for i in param_data:
                    #                 f = test_api(schedule_id, project_id, i.pk)
                    #                 if f == "success":
                    #                     temp = AutomationTestResult.objects.filter(automationScheduleApi=api_id)
                    #                 else:
                    #                     return 'fail'
                    #         param_data = json.loads(serializers.serialize('json', temp))[0]['fields']["responseData"]
                    #
                    #         param_data = get_json_value(param_data, param)
                        m = {value: param_data}
                        ##将执行结果储存下来用于提高执行效率
                        parameter_list_data.update(m)

                    except Exception as e:
                        logging.exception(e)
                        record_results(_id=_id, url=url, request_type=request_type, header=header,
                                       parameter=parameter,
                                       host=host.name,
                                       status_code=http_code, examine_type=examine_type,
                                       examine_data=response_parameter_list,
                                       _result='ERROR', code="", response_data="关联有误！", start_time=start_time,
                                       is_auto=is_auto)
                        return 'fail'

                    # elif interrelate_type == "INT" or interrelate_type == "STRING":
                    #     # TODO 如果关联参数非JSON，是INT或者STRING，此处需要修改
                    #     api_id = re.findall('(?<=<response\[Regular]\[).*?(?=\])', value)
                    #     pattern = re.findall('(?<=\[").*?(?="])', value)
                    #     param_data = json.loads(serializers.serialize(
                    #         'json',
                    #         AutomationTestResult.objects.filter(automationScheduleApi=api_id[0])))[-1]['fields'][
                    #         "responseData"]
                    #     param_data = re.findall(pattern[0], param_data.replace("\'", "\""))[0]
                    # else:
                    #     record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                    #                    host=host.name,
                    #                    status_code=http_code, examine_type=examine_type,
                    #                    examine_data=response_parameter_list,
                    #                    _result='ERROR', code="", response_data="", start_time=start_time,
                    #                    is_auto=is_auto)
                    #     return 'fail'
                    pattern = re.compile(r'<response\[.*]')
                    parameter[key_] = param_data

                else:
                    parameter[key_] = value
            except KeyError as e:
                logging.exception(e)
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               host=host.name,
                               status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                               _result='ERROR', code="", response_data="关联有误！", start_time=start_time, is_auto=is_auto)
                return 'fail'
        if data["formatRaw"]:
            request_parameter_type = "raw"

    else:
        parameter = AutomationParameterRawSerializer(AutomationParameterRaw.objects.filter(automationScheduleApi=_id),
                                                     many=True).data
        if len(parameter):
            if len(parameter[0]["data"]):
                try:
                    parameter = eval(parameter[0]["data"])
                    parameter = analysis_parameter(parameter, schedule_id, project_id)
                except Exception as e:
                    logging.exception(e)
                    record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                                   host=host.name,
                                   status_code=http_code, examine_type=examine_type,
                                   examine_data=response_parameter_list,
                                   _result='ERROR', code="", response_data="", start_time=start_time, is_auto=is_auto)
                    return 'fail'
            else:
                parameter = {}
        else:
            parameter = {}

    for i in head:
        key_ = i['fields']['name']
        value = i['fields']['value']
        if str(value).count("${")>0:
            try:
                value = get_special_parameter_value(value[2:len(value)-1], schedule_id, project_id)
                header[key_] = value
            except Exception as e:
                logging.exception(e)
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               host=host.name,
                               status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                               _result='ERROR', code="", response_data="关联有误！", start_time=start_time, is_auto=is_auto)
                return 'fail'
        # if i['fields']['interrelate']:
        #     return ""

            # try:
            #     interrelate_type = re.findall('(?<=<response\[).*?(?=\])', value)
            #     if interrelate_type[0] == "JSON":
            #         api_name = re.findall('(?<=<response\[JSON]\[).*?(?=\])', value)
            #         api_id = AutomationScheduleApi.objects.get(name=api_name[0])
            #         a = re.findall('(?<=\[").*?(?="])', value)
            #         try:
            #             param_data = eval(json.loads(serializers.serialize(
            #                 'json',
            #                 AutomationTestResult.objects.filter(automationScheduleApi=api_id.id)))[-1]['fields'][
            #                                   "responseData"])
            #             for j in a:
            #                 param_data = param_data[j]
            #         except Exception as e:
            #             logging.exception(e)
            #             record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
            #                            host=host.name,
            #                            status_code=http_code, examine_type=examine_type,
            #                            examine_data=response_parameter_list,
            #                            _result='ERROR', code="", response_data="关联有误！", start_time=start_time,
            #                            is_auto=is_auto)
            #             return 'fail'
            #     elif interrelate_type[0] == "Regular":
            #         api_id = re.findall('(?<=<response\[Regular]\[).*?(?=\])', value)
            #         pattern = re.findall('(?<=\[").*?(?="])', value)
            #         param_data = json.loads(serializers.serialize(
            #             'json',
            #             AutomationTestResult.objects.filter(automationScheduleApi=api_id[0])))[0]['fields'][
            #             "responseData"]
            #         param_data = re.findall(pattern[0], param_data.replace("\'", "\""))[0]
            #     else:
            #         record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
            #                        host=host.name,
            #                        status_code=http_code, examine_type=examine_type,
            #                        examine_data=response_parameter_list,
            #                        _result='ERROR', code="", response_data="", start_time=start_time, is_auto=is_auto)
            #         return 'fail'
            #     pattern = re.compile(r'<response\[.*]')
            #     header[key_] = re.sub(pattern, str(param_data), value)
            # except Exception as e:
            #     logging.exception(e)
            #     record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
            #                    host=host.name,
            #                    status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
            #                    _result='ERROR', code="", response_data="关联有误！", start_time=start_time, is_auto=is_auto)
            #     return 'fail'
        else:
            header[key_] = value
    try:
        if request_type == 'GET':
            code, response_data, header_data = get(header, url, request_parameter_type, parameter)
        elif request_type == 'POST':
            code, response_data, header_data = post(header, url, request_parameter_type, parameter)
        elif request_type == 'PUT':
            code, response_data, header_data = put(header, url, request_parameter_type, parameter)
        elif request_type == 'DELETE':
            code, response_data, header_data = delete(header, url, parameter)
        elif request_type == 'DUBBO':
            code, response_data, header_data = dubbo(data['host_id'], data['apiAddress'], data['dubboMethod'],
                                                     parameter)
        else:
            return 'ERROR'
    except ReadTimeout:
        logging.exception(ReadTimeout)
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter, host=host.name,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       _result='TimeOut', code="408", response_data="", start_time=start_time, is_auto=is_auto)
        return 'timeout'
    if examine_type == 'no_check':
        # response_data = json.dumps(response_data)
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter, host=host.name,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       _result='PASS', code=code, response_data=response_data, start_time=start_time, is_auto=is_auto)
        return 'success'

    elif examine_type == 'json':
        if http_code == '' or int(http_code) == code:
            if not response_parameter_list:
                response_parameter_list = "{}"
            try:
                logging.info(response_parameter_list)
                logging.info(response_data)
                result = check_json(json.loads(response_parameter_list), response_data)
                # 前端json转化需要严格格式化
                response_data = json.dumps(response_data)
            except Exception:
                logging.info(response_parameter_list)
                result = check_json(eval(
                    response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                                    response_data)
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
            return result
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'fail'

    elif examine_type == 'only_check_status':
        if http_code == '' or int(http_code) == code:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="校验HTTP状态", examine_data=response_parameter_list,
                           host=host.name, _result='PASS', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'success'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="校验HTTP状态", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'fail'

    elif examine_type == 'entirely_check':
        if http_code == '' or int(http_code) == code:
            try:
                result = operator.eq(json.loads(response_parameter_list), response_data)
            except Exception as e:
                logging.exception(e)
                result = operator.eq(eval(
                    response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                                     response_data)
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="完全校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'success'
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="完全校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'fail'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="完全校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'fail'

    elif examine_type == 'Regular_check':
        if http_code == '' or int(http_code) == code:
            try:
                logging.info(response_parameter_list)
                result = re.findall(response_parameter_list,
                                    json.dumps(response_data).encode('latin-1').decode('unicode_escape'))
                logging.info(result)
            except Exception as e:
                logging.exception(e)
                return "fail"
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'success'
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'fail'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'fail'

    elif examine_type == 'Schema_check':
        if http_code == '' or int(http_code) == code:
            try:
                response_parameter_list = json.loads(response_parameter_list)
                validate(instance=response_data, schema=response_parameter_list)
            except SchemaError as e:
                response_parameter_list = "验证模式schema出错：出错位置：{}提示信息：{}".format(" --> ".join([str(i) for i in e.path]),
                                                                               e.message)
                result = False
            except ValidationError as e:
                response_parameter_list = "json数据不符合schema规定：出错字段：{}提示信息：{}".format(" --> ".join([str(i) for i in e.path]),
                                                                                    e.message)
                result = False
            else:
                result = True
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="Schema校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'success'
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="Schema校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data,
                               start_time=start_time, is_auto=is_auto)
                return 'fail'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="Schema校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data,
                           start_time=start_time, is_auto=is_auto)
            return 'fail'

    else:
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       host=host.name, _result='FAIL', code=code, response_data=response_data, start_time=start_time,
                       is_auto=is_auto)
        return 'fail'


def get_special_parameter_value(value,schedule_id,project_id):

        value_list = re.findall('(?<=\[).*?(?=])', value)
        # 参数类型
        interrelate_type = value_list[2]
        if interrelate_type == "JSON":
            api_id = value_list[0]
            param = value_list[3]
            try:
                temp = AutomationTestResult.objects.filter(automationScheduleApi=api_id)
                if len(temp) == 0:
                    param_data = AutomationScheduleApi.objects.filter(name=api_id,
                                                                      automationTestSchedule=schedule_id)
                    for i in param_data:
                        f = test_api(schedule_id, project_id, i.pk)
                        if f == "success":
                            temp = AutomationTestResult.objects.filter(automationScheduleApi=api_id)
                        else:
                            return 'fail'
                param_data = json.loads(serializers.serialize('json', temp))[0]['fields']["responseData"]

                param_data = get_json_value(param_data, param)
                return param_data

            except  Exception as e:
                logging.exception(e)
                return e
        elif interrelate_type == "INT" or interrelate_type == "STRING":
            # TODO 如果关联参数非JSON，是INT或者STRING，此处需要修改
            api_id = re.findall('(?<=<response\[Regular]\[).*?(?=\])', value)
            pattern = re.findall('(?<=\[").*?(?="])', value)
            param_data = json.loads(serializers.serialize(
                'json',
                AutomationTestResult.objects.filter(automationScheduleApi=api_id[0])))[-1]['fields'][
                "responseData"]
            param_data = re.findall(pattern[0], param_data.replace("\'", "\""))[0]
            return param_data
        else:
            return 'fail'



def analysis_parameter(parameter,schedule_id,project_id):
    if type(parameter)==dict:
        for i in parameter:
            temp =parameter.get(i)
            if type(temp)==str:
                if temp.startswith("${"):
                    param_data = get_special_parameter_value(temp[2:len(temp)-1],schedule_id,project_id)
                    parameter[i]= param_data


            elif type(temp)==dict:
                analysis_parameter(temp,schedule_id,project_id)
            elif type(temp)==list:
                for z in range(0,len(temp)):
                    if type(temp[z]) ==dict:
                        analysis_parameter(temp[z],schedule_id,project_id)
                    if type(temp[z]) == str:
                        if temp[z].startswith("${"):
                            param_data =get_special_parameter_value(temp[z][2:len(temp[z])-1], schedule_id, project_id)
                            temp[z] = param_data
    elif type(parameter) == str:
        for i in parameter.split(";"):
            if i.split("=")[1].startswith("${"):
                param_data = get_special_parameter_value(i.split("=")[1][2:len(i.split("=")[1])-1], schedule_id, project_id)
                parameter = parameter.replace(i.split("=")[1],param_data)
    return parameter

def post(header, address, request_parameter_type, data):
    """
    post 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw' and type(data) == dict:
        data = json.dumps(data)
    response = requests.post(url=address, data=data, headers=header, timeout=60000)
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers


def get(header, address, request_parameter_type, data):
    """
    get 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw' and type(data) != dict:
        data = json.dumps(data)
    response = requests.get(url=address, params=data, headers=header, timeout=5000)
    if response.status_code == 301:
        response = requests.get(url=response.headers["location"])
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers


def put(header, address, request_parameter_type, data):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    response = requests.put(url=address, data=data, headers=header, timeout=5000)
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers


def delete(header, address, data):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param data: 请求参数
    :return:
    """
    response = requests.delete(url=address, params=data, headers=header)
    try:
        return response.status_code, response.json(), response.headers
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers


def dubbo(host_id, interface, method, parameters):
    host_value = GlobalHost.objects.get(id=host_id).host
    Host, Port = host_value.split(':')
    # 初始化dubbo对象
    conn = dubbo_telnet.connect(Host, Port)

    # 设置telnet连接超时时间
    conn.set_connect_timeout(100)

    # 设置dubbo服务返回响应的编码
    conn.set_encoding('gbk')
    common_value_str = ''
    common_value_int = ''

    if parameters.get('dubbo-str'):
        common_value_str = parameters.get('dubbo-str')
        for i in common_value_str.split(','):
            common_value_str = '"' + i + '",'
        parameters.pop('dubbo-str')
    if parameters.get('dubbo-int'):
        common_value_int = parameters.get('dubbo-int')
        for i in common_value_int.split(','):
            common_value_int = i + ','
        parameters.pop('dubbo-int')
    if len(parameters) == 0:
        param = common_value_str + common_value_int
    else:
        param = json.dumps(parameters)
        param = common_value_str + common_value_int + param
    result = conn.invoke(interface, method, param)
    try:
        result = json.loads(result)
        return {}, result, interface
    except ValueError:
        result = json.dumps({'result': result})
        return {}, result, interface

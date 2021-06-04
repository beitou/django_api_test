import django
import sys
import os

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
from django.core import serializers
from requests import ReadTimeout
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError

from api_test.common.confighttp import get, post, put, delete, dubbo
from api_test.common.common import check_json, record_auto_results
from api_test.models import AutomationScheduleApi, AutomationParameter, AutomationHead, \
    AutomationParameterRaw, AutomationScheduleTestResult
from api_test.serializers import AutomationScheduleApiSerializer, AutomationParameterRawSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def test_api(host, schedule_id, _id, time):
    """
    执行接口测试
    :param host: 测试的host域名
    :param schedule_id: 测试计划ID
    :param _id:  计划下接口ID
    :param time: 测试时间
    :return:
    """
    data = AutomationScheduleApiSerializer(AutomationScheduleApi.objects.get(id=_id, automationTestSchedule=schedule_id)).data
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
                                                          AutomationParameter.objects.filter(automationScheduleApi=_id)))
        parameter = {}

        for i in parameter_list:
            key_ = i['fields']['name']
            value = i['fields']['value']

            try:
                if i['fields']['interrelate']:
                    interrelate_type = re.findall('(?<=<response\[).*?(?=\])', value)
                    if interrelate_type[0] == "JSON":
                        api_id = re.findall('(?<=<response\[JSON]\[).*?(?=\])', value)
                        a = re.findall('(?<=\[").*?(?="])', value)
                        try:
                            param_data = eval(json.loads(serializers.serialize(
                                'json', AutomationScheduleTestResult.objects.filter(
                                    automationScheduleApi=api_id[0], testTime=time)))[0]['fields']["responseData"])
                            for j in a:
                                param_data = param_data[j]
                        except Exception:
                            record_auto_results(_id=_id, header=header, parameter=parameter,
                                                _result='ERROR', code="", response_data="关联错误！", time=time,
                                                responseHeader="{}")
                            return 'fail'
                    elif interrelate_type[0] == "Regular":
                        api_id = re.findall('(?<=<response\[Regular]\[).*?(?=\])', value)
                        pattern = re.findall('(?<=\[").*?(?="])', value)
                        param_data = json.loads(serializers.serialize(
                            'json',
                            AutomationScheduleTestResult.objects.filter(automationScheduleApi=api_id[0])))[-1]['fields']["responseData"]
                        param_data = re.findall(pattern[0], param_data.replace("\'", "\""))[0]
                    else:
                        record_auto_results(_id=_id, header=header, parameter=parameter,
                                            _result='ERROR', code="", response_data="关联错误！", time=time,
                                            responseHeader="{}")
                        return 'fail'
                    pattern = re.compile(r'<response\[.*]')
                    parameter[key_] = re.sub(pattern, param_data, value)
                else:
                    parameter[key_] = value
            except Exception as e:
                logging.exception(e)
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='ERROR', code="", response_data="", time=time, responseHeader="{}")
                return 'fail'
        if data["formatRaw"]:
            request_parameter_type = "raw"
    else:
        parameter = AutomationParameterRawSerializer(AutomationParameterRaw.objects.filter(automationScheduleApi=_id),
                                                     many=True).data
        if len(parameter[0]["data"]):
            try:
                parameter = eval(parameter[0]["data"])
            except Exception:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='ERROR', code="", response_data="", time=time, responseHeader="{}")
                return 'fail'
        else:
            parameter = []

    for i in head:
        key_ = i['fields']['name']
        value = i['fields']['value']
        if i['fields']['interrelate']:

            try:
                interrelate_type = re.findall('(?<=<response\[).*?(?=\])', value)
                if interrelate_type[0] == "JSON":
                    api_name = re.findall('(?<=<response\[JSON]\[).*?(?=\])', value)
                    api_id = AutomationScheduleApi.objects.get(name=api_name[0])
                    a = re.findall('(?<=\[").*?(?="])', value)
                    try:
                        param_data = eval(json.loads(serializers.serialize(
                            'json', AutomationScheduleTestResult.objects.filter(automationScheduleApi=api_id.id,
                                                                            testTime=time)))[0]['fields']["responseData"])
                        for j in a:
                            param_data = param_data[j]
                    except Exception as e:
                        record_auto_results(_id=_id, header=header, parameter=parameter,
                                            _result='ERROR', code="", response_data="关联错误！",
                                            time=time, responseHeader="{}")
                        return 'fail'
                elif interrelate_type[0] == "Regular":
                    api_id = re.findall('(?<=<response\[Regular]\[).*?(?=\])', value)
                    pattern = re.findall('(?<=\[").*?(?="])', value)
                    param_data = json.loads(serializers.serialize(
                        'json',
                        AutomationScheduleTestResult.objects.filter(automationScheduleApi=api_id[0])))[-1]['fields']["responseData"]
                    param_data = re.findall(pattern[0], param_data.replace("\'", "\""))[0]
                else:
                    record_auto_results(_id=_id, header=header, parameter=parameter,
                                        _result='ERROR', code="", response_data="关联错误", time=time, responseHeader="{}")
                    return 'fail'
                pattern = re.compile(r'<response\[.*]')
                header[key_] = re.sub(pattern, param_data, value)

            except Exception as e:
                logging.exception("ERROR")
                logging.error(e)
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='ERROR', code="", response_data="", time=time, responseHeader="{}")
                return 'fail'
        else:
            header[key_] = value

    # header["Content-Length"] = '%s' % len(str(parameter))
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
            code, response_data, header_data = dubbo(data['host_id'], data['apiAddress'], data['dubboMethod'], parameter)
        else:
            return 'ERROR'
    except ReadTimeout:
        record_auto_results(_id=_id, header=header, parameter=parameter,
                            _result='TimeOut', code="", response_data="", time=time, responseHeader="{}")
        return 'timeout'
    if examine_type == 'no_check':
        record_auto_results(_id=_id, header=header, parameter=parameter,
                            _result='PASS', code=code, response_data=response_data,
                            time=time, responseHeader=header_data)
        return 'success'

    elif examine_type == 'json':
        if http_code == '' or int(http_code) == code:
            # try:
            #     result = check_json(eval(response_parameter_list), response_data)
            # except:
            #     result = check_json(eval(response_parameter_list.replace('true', 'True').replace('false', 'False')),
            #                         response_data)
            if not response_parameter_list:
                response_parameter_list = "{}"
            try:
                logging.info(response_parameter_list)
                logging.info(response_data)
                result = check_json(json.loads(response_parameter_list), response_data)
            except Exception:
                logging.info(response_parameter_list)
                result = check_json(eval(response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")), response_data)
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            return result
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'only_check_status':
        if int(http_code) == code:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='PASS', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'success'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'entirely_check':
        if http_code == '' or int(http_code) == code:
            try:
                result = operator.eq(eval(response_parameter_list), response_data)
            except:
                result = operator.eq(eval(response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                                     response_data)
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'success'
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'fail'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'Regular_check':
        if http_code == '' or int(http_code) == code:
            # try:
            #     result = re.findall(response_parameter_list, json.dumps(response_data))
            # except:
            #     result = re.findall(response_parameter_list, eval(response_data.replace('true', 'True').replace('false', 'False')))
            try:
                logging.info(response_parameter_list)
                result = re.findall(response_parameter_list, json.dumps(response_data).encode('latin-1').decode('unicode_escape'))
                logging.info(result)
            except Exception as e:
                logging.exception(e)
                return "fail"
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'success'
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'fail'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'Schema_check':
        if http_code == '' or int(http_code) == code:
            try:
                response_parameter_list = json.loads(response_parameter_list)
                validate(instance=response_data, schema=response_parameter_list)
            except SchemaError as e:
                header = "验证模式schema出错：\n出错位置：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message)
                result = False
            except ValidationError as e:
                header = "json数据不符合schema规定：\n出错字段：{}\n提示信息：{}".format(" --> ".join([i for i in e.path]), e.message)
                result = False
            else:
                result = False
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            return result
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    else:
        record_auto_results(_id=_id, header=header, parameter=parameter,
                            _result='FAIL', code=code, response_data=response_data,
                            time=time, responseHeader=header_data)
        return 'fail'

import logging

import requests
import xlrd
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.utils import json
from rest_framework.views import APIView
from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic, record_caseDynamic
from api_test.models import Project, ApiInfo, ApiHead, ApiParameter, ApiParameterRaw, ApiResponse, ApiOperationHistory, \
    CaseProject, CaseInfo, CaseRequirement, CaseOperationHistory
from django.db import transaction

from api_test.serializers import ApiInfoDeserializer, ApiHeadDeserializer, ApiParameterDeserializer, \
    ApiResponseDeserializer, CaseProjectSerializer, CaseDeserializer, CaseRequirementDeserializer

logger = logging.getLogger( __name__ )  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class ImportCaseFromExcel(APIView):
    """
    导入测试用例
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验必传参数
            if not data["caseProject_id"] or not data["requirementName"]:
                return JsonResponse(code="999996", msg="参数有误!")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误!")

    def post(self, request):
        # data = JSONParser().parse(request)
        data = request.data
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = CaseProject.objects.get(id=data["caseProject_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在!")
        pro_data = CaseProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obk = CaseRequirement.objects.filter(name=data["requirementName"], yn=0)
        # 存在则继续，不存在则创建
        if obk.exists():
            caseRequirement_id = obk[0].id
        else:
            requirement_data = {"name": data["requirementName"],
                                "caseProject_id": data["caseProject_id"],
                                "user": request.user.pk,
                                "zentao_id": data["zentao_id"]}
            caseRequirement_serializer = CaseRequirementDeserializer(data=requirement_data)
            with transaction.atomic():
                if caseRequirement_serializer.is_valid():
                    # 保存新需求
                    caseRequirement_serializer.save(caseProject=obj)
                    caseRequirement_id = caseRequirement_serializer.data.get("id")
                    # 记录动态
                    record_caseDynamic(caseProject=caseRequirement_serializer.data.get("id"),
                                       _type="添加", operationObject="需求", user=request.user.pk,
                                       data=data["requirementName"])
                else:
                    return JsonResponse(code="999998", msg="失败")
        errList = []
        if data["file"]:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=data["file"].name, file_contents=data["file"].read())
            table = wb.sheets()[0]
            rows = table.nrows
            for x in range(1, rows):
                row = table.row_values(x)
                case_data = {"priority": row[1].lower(),  # 第二列优先级 必填
                             "name": row[4].strip(),  # 第五列用例名称 必填，且唯一
                             "testType": row[2],  # 第三列测试类型 非必填
                             "testTontent": row[3], # 测试内容 非必填
                             "caseProject_id": data["caseProject_id"],
                             "caseRequirement_id": caseRequirement_id,
                             "operationSteps": row[5],  # 第六列操作步骤 必填
                             "expectedResults": row[6],  # 第七列预期结果 必填
                             "actualResult": int(row[7]) if row[7] else 0,  # 第八列实际结果 非必填 内容为0，1，2
                             "reason": row[8],  # 第九列原因 非必填
                             "version": row[10],  # 第十一列版本 非必填
                             "hardware": row[11],  # 第十二列硬件 非必填
                             "userUpdate": request.user.pk,
                             "stage": ['1']}
                case_name = CaseInfo.objects.filter(name=case_data["name"], caseProject=case_data["caseProject_id"],
                                                    caseRequirement_id=case_data["caseRequirement_id"], yn=0)
                if len(case_name):
                    errList.append("存在相同名称!用例名:" + case_data["name"] + ",第" + str(x + 1) + "行")
                    continue
                    #return JsonResponse(code="999997", msg="存在相同名称!"+case_data["name"])
                else:
                    with transaction.atomic():  # 执行错误后，帮助事物回滚
                        serialize = CaseDeserializer(data=case_data)
                        if serialize.is_valid():
                            try:
                                if not isinstance(case_data.get("caseRequirement_id"), int):
                                    return JsonResponse(code="999996", msg="参数有误!")
                                obi = CaseRequirement.objects.get(id=case_data["caseRequirement_id"],
                                                                  caseProject=case_data["caseProject_id"])
                                serialize.save(caseProject=obj, caseRequirement=obi)
                            except KeyError:
                                serialize.save(caseProject=obj)
                            except ObjectDoesNotExist:
                                return JsonResponse(code="999991", msg="需求不存在!")
                            case_id = serialize.data.get("id")
                            record_caseDynamic(caseProject=data["caseProject_id"],
                                               _type="导入", operationObject="用例", user=request.user.pk,
                                               data="导入用例“%s”" % case_data["name"])
                            case_record = CaseOperationHistory(case=CaseInfo.objects.get(id=case_id),
                                                               user=User.objects.get(id=request.user.pk),
                                                               description="导入用例“%s”" % case_data["name"])
                            case_record.save()
                        else:
                            errList.append("参数有误!excel第" + str(x + 1) + "行")
            if len(errList) > 0:
                return JsonResponse(code="999996", msg="部分成功!<br/>" + "<br/>".join(errList))
            return JsonResponse(code="999999", msg="成功!")
        return JsonResponse(code="999996", msg="参数有误!")


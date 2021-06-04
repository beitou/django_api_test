#!/usr/bin/env python
# coding:utf-8
import logging
from io import BytesIO

import xlwt
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caseProjectExport")# project_name 项目名称

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from rest_framework.views import APIView

from api_test import serializers
from api_test.common import zentao
from api_test.common.api_response import JsonResponse
from api_test.common.common import record_caseDynamic
from api_test.models import CaseProject, CaseRequirement
from api_test.serializers import CaseProjectSerializer, CaseRequirementDeserializer

logger = logging.getLogger( __name__ )  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。

class ExportCaseExcel(APIView):
    """
    导出测试用例
    """
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

    def post(self, request, list_obj=0):
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
        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=' + data + '.xls'

        def get(self, request):

            # 返回前所有商品的前10条数据
            zentao_list = zentao.objects.all()[:10]
            # 直接转换成json类型的字符串
            data = serializers.serialize("json", zentao_list)
            # 注意要加上："application/json"，否则在浏览器显示不正常
            return HttpResponse(data, "application/json")

        if list_obj:
            # 创建工作簿
            ws = xlwt.Workbook(encoding='utf-8')
            # 添加第一页数据表
            w = ws.add_sheet('测试用例')  # 新建sheet（sheet的名称为"sheet1"）
            # 写入表头
            w.write(0, 0, u'用例编号')
            w.write(0, 1, u'优先级')
            w.write(0, 2, u'测试类型')
            w.write(0, 3, u'测试内容')
            w.write(0, 4, u'用例名称')
            w.write(0, 5, u'操作步骤')
            w.write(0, 6, u'预期结果')
            w.write(0, 7, u'实际结果')
            w.write(0, 8, u'原因')
            w.write(0, 9, u'版本')
            w.write(0, 9, u'硬件')
            excel_row = 1
            for obj in list_obj:
                caseRequirement_id = caseRequirement_id
                priority = obj.priority
                no = obj.no
                testType = obj.testType
                content = obj.content
                name = obj.name
                operationSteps = obj.operationSteps
                expectedResults = obj.expectedResults
                actualResult = obj.actualResult
                reason = obj.reason
                version = obj.version
                hardware = obj.hardware
                # 写入每一行对应的数据
                w.write(excel_row, 0, no)  #用例编号
                w.write(excel_row, 1, priority) #优先级
                w.write(excel_row, 2, testType) #测试类型
                w.write(excel_row, 3, content) #测试内容
                w.write(excel_row, 4, name) #用例名称
                w.write(excel_row, 5, operationSteps) #操作步骤
                w.write(excel_row, 6, expectedResults) #预期结果
                w.write(excel_row, 7, actualResult) #实际结果
                w.write(excel_row, 8, reason) #原因
                w.write(excel_row, 9, version) #版本
                w.write(excel_row, 10, hardware) # 硬件
                excel_row += 1
            # 写出到IO
            output = BytesIO()
            ws.save(output)
            # 重新定位到开始
            output.seek(0)
            JsonResponse.write(output.getvalue())
        return JsonResponse










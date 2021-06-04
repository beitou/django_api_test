import logging

import xlrd
import xlsxwriter
from django.core.checks import messages

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CaseWrite:
    def __init__(self, project_name):
        self.workbook = xlsxwriter.Workbook(project_name)
        self.worksheet = self.workbook.add_worksheet()
        bold = self.workbook.add_format({'bold': True})
        self.worksheet.write(0, 0, "用例编号（非必填）", bold)
        self.worksheet.write(0, 1, "优先级（必填p1,p2,p3）", bold)
        self.worksheet.write(0, 2, "测试类型(非必填)", bold)
        self.worksheet.write(0, 3, "测试内容（非必填）", bold)
        self.worksheet.write(0, 4, "用例名称（必填，且唯一）", bold)
        self.worksheet.write(0, 5, "操作步骤（必填）", bold)
        self.worksheet.write(0, 6, "预期结果（必填）", bold)
        self.worksheet.write(0, 7, "实际结果（非必填，若需填写只支持填0，1，2）", bold)
        self.worksheet.write(0, 8, "原因（非必填）", bold)
        self.worksheet.write(0, 9, "测试日期（非必填）", bold)
        self.worksheet.write(0, 10, "版本（非必填）", bold)
        self.worksheet.write(0, 11, "硬件（非必填）", bold)

    def case_write_schedule(self, data=None):
        if not data:
            return True
        row = 1

        for i in data:
            self.worksheet.write(row, 0, row)
            self.worksheet.write(row, 1, i["priority"])
            self.worksheet.write(row, 2, i["testType"])
            self.worksheet.write(row, 3, i["testTontent"])
            self.worksheet.write(row, 4, i["name"])
            self.worksheet.write(row, 5, i["operationSteps"])
            self.worksheet.write(row, 6, i["expectedResults"])
            self.worksheet.write(row, 7, i["actualResult"])
            self.worksheet.write(row, 8, i["reason"])
            self.worksheet.write(row, 9, i["createTime"])
            self.worksheet.write(row, 10, i["version"])
            self.worksheet.write(row, 11, i["hardware"])
            row = row + 1
        self.workbook.close()
        return True





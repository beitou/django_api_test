import logging

import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from xpinyin import Pinyin

from api_test.common.api_response import JsonResponse
from requests import RequestException

from api_test.common.name_mapping import get_team_name
from api_test.common.gitlab_api import GitLabApi
from api_test.common.name_mapping import get_git_name
from api_test.common.zentao import ZenTao

logger = logging.getLogger(__name__) # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class CodeQuality(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    # def paixu(self, i):
    #     i = dict(sorted(i.items(), key=lambda x: x[1], reverse=False))
    #     return i

    def get(self, request):
        startTime = request.GET.get("startTime")
        endTime = request.GET.get("endTime")
       # 千行代码bug率
        codeQualith = {}
        try:
            g = GitLabApi(0, startTime, endTime)
            userSubmit = g.getAllLins()
            print("代码行数", userSubmit)
            userSubmit = dict(sorted(userSubmit.items(), key=lambda x: x[1], reverse=False))
            print("代码行数排序后", userSubmit)
            s = requests.session()
            z = ZenTao(s, 'yunyi', 'Ma970825', '0', startTime, endTime)
            z.get_zentaosid()
            bug_count = z.count_bugs()
            resolved_dict = bug_count.get('resolved_dict')
            resolved_dict = dict(sorted(resolved_dict.items(), key=lambda x: x[1], reverse=False))
            # 人员解决bug总时长
            solution_times = bug_count.get('solution_times')
            print("拿到数据", solution_times)
            # 计算人员解决bug平均时长 单位：小时
            for key in solution_times:
                solution_times.update({key: round(float(solution_times.get(key)/resolved_dict.get(key)), 2)})
            print("平均时长", solution_times)
            # 人员日清bug数
            daily_clearance_rates = bug_count.get('daily_clearance_rates')
            print("正常计算前", daily_clearance_rates)
            for key in daily_clearance_rates:
                daily_clearance_rates.update({key: round(float(daily_clearance_rates.get(key)/float((resolved_dict.get(key)
                                                                                                  ) / float(100))), 2)})
            daily_clearance_rates = dict(sorted(daily_clearance_rates.items(), key=lambda x: x[1], reverse=False))
            print("正常计算后", daily_clearance_rates)
            # 计算千行代码bug率
            for i in userSubmit:
                if i in resolved_dict.keys():
                    if userSubmit.get(i) != 0:
                        codeQualith.update(
                            # {i + '-' + str(userSubmit.get(i)): str(round(float(resolved_dict.get(i)) / (float(userSubmit.get(i)) / float(1000)), 2))})
                            {i: round(float(resolved_dict.get(i)) / (float(userSubmit.get(i)) / float(1000)), 2)})
            codeQualith = dict(sorted(codeQualith.items(), key=lambda x: x[1], reverse=False))
            userSubmit = get_team_name(userSubmit)
            userSubmit.keys()
            resolved_dict = get_team_name(resolved_dict)
            codeQualith = get_team_name(codeQualith)
            solution_times = dict(sorted(solution_times.items(), key=lambda x: x[1], reverse=False))
            print("排序后", solution_times)
            solution_times = get_team_name(solution_times)
            print("分组后", solution_times)
            daily_clearance_rates = get_team_name(daily_clearance_rates)

        except RequestException:
            return JsonResponse(code="999998", msg="请求失败!")
        return JsonResponse(data={"userSubmit": userSubmit, 'codeQualith': codeQualith, 'resolved_dict': resolved_dict, 'solution_times': solution_times, 'daily_clearance_rates': daily_clearance_rates}, code="999999", msg="成功")

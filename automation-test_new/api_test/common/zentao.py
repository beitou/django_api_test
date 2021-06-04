import json
import re
from datetime import datetime
import requests

from api_automation_test import settings
from api_test.common.name_mapping import get_git_name
from api_test.common.name_mapping import get_team_name

getSessionPath = settings.SESSIONID_PATH
userLoginPath = settings.USERLOGIN_PATH
bugPath = settings.BUG_PATH
zenTaoPath = settings.ZENTAO_PATH


class ZenTao:

    def __init__(self, s, username, password, id, since=None, until=None, search_id=None):
        self.s = s
        self.username = username
        self.password = password
        self.id = id
        self.since = since
        self.until = until
        self.search_id = search_id

    def get_sessions(self):
        """
         获取登录页的sessions api
         :return:
         """
        url = getSessionPath
        getsessionid = self.s.get(url)
        getsessionid_str = json.loads(getsessionid.content)
        sessionID = json.loads(getsessionid_str['data'])["sessionID"]
        return sessionID

    # def getSessionID(self):
    #     """
    #     获取SessionID
    #     :return:
    #     """
    #     # response = urllib.request.urlopen(getSessionPath)
    #     # html = response.read().decode('utf-8')
    #     session = requests.Session()
    #     response = session.get(url=getSessionPath)
    #     html = response.text.encode('utf-8')
    #     params = json.loads(html)
    #     data = json.loads(params['data'])
    #     print(data['sessionID'])

    def get_zentaosid(self):
        """
        用户登录api
        :return:
        """
        url = userLoginPath + self.get_sessions()
        data = {"account": self.username, "password": self.password}
        req = self.s.post(url, data=data)
        get_zentaosid_str = json.loads(req.content)
        return get_zentaosid_str

    # def userLogin(self):
    #     session = requests.Session()
    #     session.get(url=getSessionPath)
    #     data = {'account': 'mingxi', 'password': 'hlj@123'}
    #     response = requests.post(url=userLoginPath, data=data)
    #     html = response.text.encode('utf-8')
    #     params = json.loads(html)
    #     print(params['user']['realname'])

    def get_bugs(self):
        """
        获取所有BUG
        :return:
        """
        if self.since is not None:
            self.buildQuery()
            url = zenTaoPath + "zentao/bug-browse-" + self.id + "-0-bySearch-" + self.search_id + "--2000-2000-1.json"
            loginResp = json.loads(self.s.get(url).content)
            data = loginResp['data']
            data_json = json.loads(data)['bugs']
        else:
            url = bugPath + self.id + "-0-all-0-id_desc-2000-2000-1.json"
            loginResp = json.loads(self.s.get(url).content)
            data = loginResp['data']
            data_json = json.loads(data)['bugs']
        return data_json

    def bugs_lists(self):
        """
        对获取的BUG处理，过滤出需要的字段，重新返回列表bugs_list
        :return:
        """
        bugs_list = []
        for bug in self.get_bugs():
            title = bug['title']
            severity = bug['severity']
            status = bug['status']
            resolvedBy = bug['resolvedBy']
            openedDate = bug['openedDate']
            resolvedDate = bug['resolvedDate']
            bug_dict = {'title': title, 'severity': severity, 'status': status, 'resolvedBy': resolvedBy, 'openedDate': openedDate, 'resolvedDate': resolvedDate}
            bugs_list.append(bug_dict)
        return bugs_list

    # def time(self, bug):
    #     days = (datetime.strptime(bug['resolvedDate'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'],
    #                                                                                             "%Y-%m-%d %H:%M:%S")).days
    #     seconds = (datetime.strptime(bug['resolvedDate'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'],
    #                                                                                                "%Y-%m-%d %H:%M:%S")).seconds
    #     return days, seconds

    def daily_clearance_rate(self, bug, daily_clearance_rates):
        days = (datetime.strptime(bug['resolvedDate'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'],
                                                                                                "%Y-%m-%d %H:%M:%S")).days
        if days >= 1:
            daily_clearance_rates[get_git_name(bug['resolvedBy'])] += 1
        return daily_clearance_rates

    # 计算bug处理时间：由bug创建至bug关闭的时间，单位：小时
    def solution_time(self, bug, solution_times):
        days = (datetime.strptime(bug['resolvedDate'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'],
                                                                                                "%Y-%m-%d %H:%M:%S")).days
        seconds = (datetime.strptime(bug['resolvedDate'],"%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'],
                                                                                                "%Y-%m-%d %H:%M:%S")).seconds
        # a = self.time(bug)
        solution_time = days * 24 + seconds / 3600
        # solution_time = ((datetime.strptime(bug['resolvedDate'], "%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'], "%Y-%m-%d %H:%M:%S")).days * 24 * 60 + ((datetime.strptime(bug['resolvedDate'],"%Y-%m-%d %H:%M:%S") - datetime.strptime(bug['openedDate'], "%Y-%m-%d %H:%M:%S")).seconds / 60))/60
        solution_times[get_git_name(bug['resolvedBy'])] += solution_time
        # if days >= 1:
        #     daily_clearance_rates[get_git_name(bug['resolvedBy'])] += 1
        return solution_times

    def count_bugs(self):
        """
        需要的数据：功能项，BUG各状态条数，BUG状态对应的关闭数
        输入：功能项标题
        统计：BUG各状态计数，BUG状态下关闭数计数
        输出：所有功能项对应统计数，列表显示，如：
        :return:
        """
        s_1_status_closed_count = 0
        s_2_status_closed_count = 0
        s_3_status_closed_count = 0
        s_4_status_closed_count = 0

        severity_1_count = 0
        severity_2_count = 0
        severity_3_count = 0
        severity_4_count = 0
        empty_count = 1
        bugs_list = self.bugs_lists()
        resolved_dict = {}
        solution_times = {}
        daily_clearance_rates = {}

        for bug in bugs_list:
            if bug['severity'] == '1':
                severity_1_count += 1
                if bug['status'] == 'closed':
                    s_1_status_closed_count += 1
            elif bug['severity'] == '2':
                severity_2_count += 1
                if bug['status'] == 'closed':
                    s_2_status_closed_count += 1
            elif bug['severity'] == '3':
                severity_3_count += 1
                if bug['status'] == 'closed':
                    s_3_status_closed_count += 1
            elif bug['severity'] == '4':
                severity_4_count += 1
                if bug['status'] == 'closed':
                    s_4_status_closed_count += 1
            if bug['status'] == 'closed':
                if get_git_name(bug['resolvedBy']) in resolved_dict.keys():
                    resolved_dict[get_git_name(bug['resolvedBy'])] += 1
                    solution_times = self.solution_time(bug, solution_times)
                    daily_clearance_rates = self.daily_clearance_rate(bug, daily_clearance_rates)
                elif get_git_name(bug['resolvedBy']) == "":
                    resolved_dict.update({'weizhi': empty_count})
                    empty_count += 1
                else:
                    resolved_dict.update({get_git_name(bug['resolvedBy']): 1})
                    solution_times.update({get_git_name(bug['resolvedBy']): 0})
                    daily_clearance_rates.update({get_git_name(bug['resolvedBy']): 0})
                    solution_times = self.solution_time(bug, solution_times)
                    daily_clearance_rates = self.daily_clearance_rate(bug, daily_clearance_rates)

        # resolved_dict = json.dumps(resolved_dict)
        total = len(bugs_list)
        closed = s_1_status_closed_count + s_2_status_closed_count + s_3_status_closed_count + s_4_status_closed_count
        bug_count = {"total": total,
                     "closed": closed,
                     "p1": severity_1_count,
                     "p2": severity_2_count,
                     "p3": severity_3_count,
                     "p4": severity_4_count,
                     "closed_rate": '%.2f' % (closed / total * 100),
                     "resolved_dict": resolved_dict,
                     "solution_times": solution_times,
                     "daily_clearance_rates": daily_clearance_rates
                     # "team_bug_count": team_bug_count,
                     # "team_closed_rate": '%.2f' % (team_bug_count / total * 100)
                     }
        return bug_count

    # 团队bug数
    def team_bugs(self):
        bugs_list = self.bugs_lists()
        team_bug_count = {}
        empty_count_team = 1
        for bug in bugs_list:
            if bug['status'] == 'closed':
                if get_team_name(bug['resolvedBy']) in team_bug_count.keys():
                    team_bug_count[get_team_name(bug['resolvedBy'])] += 1
                elif get_team_name(bug['resolvedBy']) == "":
                    team_bug_count.update({'weizhi1': empty_count_team})
                    empty_count_team += 1
                else:
                    team_bug_count.update({get_team_name(bug['resolvedBy']): 1})
        bug_count_team = {"team_bug_count": team_bug_count}
        return bug_count_team

    def buildQuery(self):
        url = zenTaoPath + 'zentao/search-buildQuery.json'
        data = {"fieldtitle": "", "fieldkeywords": "", "fieldsteps": "", "fieldassignedTo": "", "fieldresolvedBy": "",
                "fieldstatus": "", "fieldconfirmed": "ZERO", "fieldproduct": 131, "fieldplan": "",
                "fieldmodule": "ZERO", "fieldproject": "", "fieldseverity": 0, "fieldpri": 0, "fieldtype": "",
                "fieldos": "", "fieldbrowser": "", "fieldresolution": "", "fieldactivatedCount": "", "fieldtoTask": "",
                "fieldtoStory": "", "fieldopenedBy": "", "fieldclosedBy": "", "fieldlastEditedBy": "",
                "fieldmailto": "", "fieldopenedBuild": "", "fieldresolvedBuild": "", "fieldopenedDate": "",
                "fieldassignedDate": "", "fieldresolvedDate": "", "fieldclosedDate": "", "fieldlastEditedDate": "",
                "fielddeadline": "", "fieldid": "", "andOr1": "AND", "field1": "product", "operator1": "",
                "value1": "all", "andOr2": "and", "field2": "openedDate", "operator2": "<", "value2": self.until,
                "andOr3": "and", "field3": "keywords", "operator3": "include", "value3": "", "groupAndOr": "and",
                "andOr4": "AND", "field4": "openedDate", "operator4": ">", "value4": self.since, "andOr5": "and",
                "field5": "assignedTo", "operator5": "", "value5": "", "andOr6": "and", "field6": "resolvedBy",
                "operator6": "", "value6": "", "module": "bug",
                "actionURL": "/zentao/bug-browse-131-0-bySearch-myQueryID.html", "groupItems": 3, "formType": "more"}
        self.s.post(url, data=data)
        self.saveQuery()

    def saveQuery(self):
        url = zenTaoPath + 'zentao/search-saveQuery-bug-yes.json'
        data = {"title": self.since + "至" + self.until, "module": "bug"}
        result = self.s.post(url, data=data)
        self.search_id = re.findall('(?<=loadQueries\().*?(?=\,)', str(result.content))[0]

#'(?<=loadQueries\().*?(?=\,)
# if __name__ == "__main__":
# #     userLogin()
#     s = requests.session()
#     z = ZenTao(s, 'mingxi', 'hlj@123', '131', '2020-04-01', '2020-06-30')
#     z.get_zentaosid()
#     z.buildQuery()
# #     # print(z.bugs_lists())
# #     # print(z.count_bugs())
#     print(z.team_bugs())

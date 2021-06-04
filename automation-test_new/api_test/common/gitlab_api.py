import json
import re

import requests
import xlrd
import csv
from xpinyin import Pinyin
from api_automation_test import settings
from api_test.common.name_mapping import get_git_name, abandon_git_name
import time

private_host = settings.GITLAB_PATH
private_token = settings.GITLAB_TOKEN


class GitLabApi:

    def __init__(self, project_id='0', since='', until=''):
        self.since = since
        self.until = until
        self.project_id = project_id

    def get100Commits(self, page):
        """
        分批获取commit
        :param page:
        :return:
        """
        url = private_host + '/api/v4/projects/' + str(self.project_id) + '/repository/commits?private_token=' + private_token + '&since=' + self.since + '&until=' + self.until + '&with_stats=true' + '&all=true' + '&per_page=100' + '&page=' + str(page)
        # print(url)
        r = requests.get(url)
        data = r.json()
        commits = []
        for i in data:
            if 'author_name' in i:
                commit = {}
                commit['author_name'] = i['author_name']
                commit['total'] = i['stats']['total']
                commits.append(commit)
        return commits

    def getAllCommits(self):
        """
        获取所有项目下提交
        :return:
        """
        page = 1
        commits = []
        donext = True
        while donext:
            pros = self.get100Commits(page)
            for pro in pros:
                commits.append(pro)
            page = page+1
            if len(pros) < 100:
                donext = False
        return commits

    def getLines(self):
        """
        获取一个项目所有提交行数
        :return:
        """
        userSubmit = {}
        commits = self.getAllCommits()
        for commit in commits:
            if commit['author_name'] in userSubmit.keys():
                userSubmit[commit['author_name']] += commit['total']
            else:
                userSubmit.update({commit['author_name']: commit['total']})
        return userSubmit

    def getAllGit(self):
        """
        获取所有git名称
        :return:
        """
        projects = []
        with open('/Users/cc/Downloads/result.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i, line in enumerate(reader):
                if i > 0 and line[1] != 'NULL':
                    name = re.search(r'([^/]+)(?=\.git)', line[1]).group()
                    projects.append(name)
        return projects

    def getAllId(self):
        """
        已废弃
        :param page:
        :return:
        """
        projects = self.getAllGit()
        projectId = []
        for name in projects:
            url = private_host + '/api/v4/projects?private_token=' + private_token + '&search=' + name
            r = requests.get(url)
            data = r.json()
            for i in data:
                if i['id'] not in projectId:
                    projectId.append(i['id'])
        groupId = [3, 82, 17, 40, 33, 22]
        for group in groupId:
            url = private_host + '/api/v4/groups/' + str(group) + '/projects?private_token=' + private_token
            r = requests.get(url)
            data = r.json()
            for i in data:
                if i['id'] not in projectId:
                    projectId.append(i['id'])
        return projectId

    def getAllProjectLins(self):
        page = 1
        projects = []
        donext = True
        while donext:
            pros = self.get100Project(page)
            for pro in pros['projects']:
                projects.append(pro)
            page = page + 1
            if pros['pro'] < 100:
                donext = False
        return projects

    def get100Project(self, page):
        """
        分批获取project
        :param page:
        :return:
        """
        url = private_host + '/api/v4/projects?private_token=' + private_token + '&simple=true' + '&per_page=100' + '&page=' + str(page)
        r = requests.get(url)
        data = r.json()
        projects = []
        pros = {}
        for i in data:
            if 'id' in i:
                if time.strptime(i['last_activity_at'][0:10], "%Y-%m-%d") >= time.strptime(self.since, "%Y-%m-%d"):
                    projects.append(i['id'])
        pros['projects'] = projects
        pros['pro'] = len(data)
        return pros

    def getAllLins(self):
        """
        获取所有的代码
        :return:
        """
        # projectId = self.getAllId()
        p = Pinyin()
        projectId = self.getAllProjectLins()
        # projectId = [1151, 1150, 822, 820, 1039, 77, 625, 385, 434, 415, 412, 452, 447, 413, 390, 379, 368, 579, 782, 432, 419, 438, 360, 204, 469, 418, 417, 436, 435, 475, 484, 769, 373, 425, 346, 449, 423, 486, 458, 429, 430, 779, 433, 440, 589, 416, 375, 377, 750, 696, 655, 649, 424, 448, 428, 381, 422, 547, 525, 524, 421, 631, 659, 414, 638, 454, 431, 441, 455, 800, 854, 528, 468, 472, 470, 466, 383, 467, 465, 624, 460, 462, 461, 485, 1057, 845, 172, 480, 479, 478, 471, 482, 463, 408, 672, 477, 437, 580, 523, 476, 474, 593, 372, 83, 67, 371, 602, 859, 853, 723, 722, 885, 892, 1216, 1176, 1120, 1119, 1067, 1052, 924, 839, 837, 1193, 473, 542, 600, 601, 886, 920, 532, 963, 988, 717, 1023, 995, 922, 1220, 993, 923, 991, 1062, 1028, 1033, 1034, 1037, 1042, 1040, 1036, 1074, 1006, 1007, 1055, 1024, 1069, 1049, 491, 1109, 1088, 1089, 1053, 1093, 1090, 1121, 1124, 1110, 1134, 1139, 1173, 1171, 568, 282, 1181, 1178, 1186, 1202, 1204, 1203, 1211, 1215, 1174, 1225, 1229, 1219, 1209, 1197, 1192, 1170, 1168, 1149, 1137, 1129, 1127, 1123, 1118, 1117, 1102, 1086, 1068, 1063, 1056, 894, 872, 860, 378, 221, 217, 202, 1228, 1224, 1179, 1103, 1096, 1017, 927, 828, 804, 792, 367, 350, 302, 297, 291, 238, 216, 199, 180, 178, 768, 572, 220, 52, 1143, 1097, 1077, 1018, 1014, 982, 979, 978, 976, 973, 962, 952, 951, 934, 933, 932, 929, 907, 905]
        # projectId = [993,995,827,839,562,554,375,455,416,580,1037,1075,1069,1057,448,1092,1121]
        # print(len(projectId))
        userSubmit = {}
        for id in projectId:
            self.project_id = id
            commits = self.getAllCommits()
            for commit in commits:
                if commit['author_name'] in abandon_git_name():
                    continue
                if commit['total'] > 3000:
                    continue
                for ch in commit['author_name']:
                    # 中文转英文
                    if u'\u4e00' <= ch <= u'\u9fff':
                        commit['author_name'] = p.get_pinyin(commit['author_name'], '')
                        break
                commit['author_name'] = get_git_name(commit['author_name'])
                # 统计
                if commit['author_name'] in userSubmit.keys():
                    userSubmit[commit['author_name']] += commit['total']
                else:
                    userSubmit.update({commit['author_name']: commit['total']})
        return userSubmit


if __name__ == "__main__":
    g = GitLabApi('product-gateway', '2020-03-09', '2020-03-13')
    # print(g.getAllId())
    # print(g.getAllLins())
    # print(g.getLines())
    print(g.getAllProjectLins())




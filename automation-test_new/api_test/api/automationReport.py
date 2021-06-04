from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,Count
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.models import Project, AutomationTaskRunTime, AutomationTestSchedule, AutomationScheduleApi, \
    AutomationScheduleTestResult
from api_test.serializers import AutomationAutoTestResultSerializer, \
    AutomationTestLatelyTenTimeSerializer, AutomationTaskRunTimeSerializer, ProjectSerializer,AutomationTestScheduleSerializer


# class TestTime(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = ()
#
#     def get(self, request):
#         """
#         获取执行测试时间
#         :param request:
#         :return:
#         """
#         project_id = request.GET.get("project_id")
#         if not project_id:
#             return JsonResponse(code="999996", msg="参数有误！")
#         if not project_id.isdecimal():
#             return JsonResponse(code="999996", msg="参数有误！")
#         try:
#             pro_data = Project.objects.get(id=project_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(code="999995", msg="项目不存在！")
#         pro_data = ProjectSerializer(pro_data)
#         if not pro_data.data["status"]:
#             return JsonResponse(code="999985", msg="该项目已禁用")
#         try:
#             data = AutomationTaskRunTimeSerializer(
#                 AutomationTaskRunTime.objects.filter(project=project_id).order_by("-startTime")[:10],
#                 many=True).data
#         except IndexError:
#             data = AutomationTaskRunTimeSerializer(
#                 AutomationTaskRunTime.objects.filter(project=project_id).order_by("-startTime"),
#                 many=True).data
#         return JsonResponse(code="999999", msg="成功！", data=data)


class AutoTestReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        测试结果报告
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")

        if not project_id or not start_time or not end_time:
            return JsonResponse(code="999996", msg="参数有误！")
        if not project_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obj = AutomationTestSchedule.objects.filter(project=project_id)
        # 每个场景的接口个数-DONE
        ATSSerializer = AutomationTestScheduleSerializer(obj, many=True).data
        print(ATSSerializer)
        ATSSerializer_map = {x['id']: x['api_count'] for x in ATSSerializer}

        if obj:
            schedule = Q()
            for i in obj:
                schedule = schedule | Q(automationTestSchedule=i.pk)
            schedule_data = AutomationScheduleApi.objects.filter(schedule)

            api = Q()
            if schedule_data:
                for j in schedule_data:
                    api = api | Q(automationScheduleApi=j.pk)
                # AutoSerializer = AutomationScheduleApiSerializer(schedule_data,many=True).data
                ##总场景信息 - DONE，场景成功次数 - DONE，场景失败次数 - DONE
                task_run_time = AutomationTaskRunTimeSerializer(
                    AutomationTaskRunTime.objects.filter(project=project_id, startTime__gte=start_time,
                                                         startTime__lte=end_time), many=True).data

                test_scenario_name = []
                test_scenario = []

                for i in task_run_time:
                    if i['Schedule_name'] not in test_scenario_name:
                        test_scenario_name.append(i['Schedule_name'])
                        temp = [i['Schedule_id'], 0, 0, i['Schedule_name']]

                        test_scenario.append(temp)
                    for x in test_scenario:
                        if i["Schedule_name"] in x:
                            if i["result"] == 'PASS':
                                x[1] = x[1] + 1
                                x[2] = x[2] + 1
                            else:
                                x[2] = x[2] + 1

                print(test_scenario)

                scenario_data = []
                for x in test_scenario:
                    temp = {
                        "scenario_name": x[3],
                        "scenario_api_count": ATSSerializer_map.get(int(x[0])),
                        "success_count": x[1],
                        "fail_count": x[2] - x[1],
                        "total_count": x[2],
                    }
                    scenario_data.append(temp)
                print(scenario_data)
                all_data = AutomationAutoTestResultSerializer(
                    AutomationScheduleTestResult.objects.filter(api, testTime__gte=start_time, testTime__lte=end_time),
                    many=True).data
                fail_data = AutomationScheduleTestResult.objects.filter(api, testTime__gte=start_time,
                                                                        testTime__lte=end_time, result='FAIL').values(
                    'automationScheduleApi', 'automationScheduleApi__name').annotate(
                    a=Count("automationScheduleApi")).order_by("a")

                fail_data_list = []
                for n in fail_data:
                    temp = {
                        'api_name': n['automationScheduleApi__name'],
                        'api_count': n['a']
                    }
                    fail_data_list.append(temp)
                print(fail_data_list)
                return JsonResponse(code="999999", msg="成功！", data={"data": all_data,
                                                                    "scenario_data": scenario_data,
                                                                    "fail_data": fail_data_list,
                                                                    })
            else:
                return JsonResponse(code="999999", msg="成功！")
        else:
            return JsonResponse(code="999987", msg="计划不存在！")


# class AutoLatelyTenTime(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = ()
#
#     def get(self, request):
#         """
#         获取最近十次的测试数据
#         project_id 项目ID
#         :param request:
#         :return:
#         """
#         project_id = request.GET.get("project_id")
#         if not project_id:
#             return JsonResponse(code="999996", msg="参数有误！")
#         if not project_id.isdecimal():
#             return JsonResponse(code="999996", msg="参数有误！")
#         try:
#             pro_data = Project.objects.get(id=project_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(code="999995", msg="项目不存在！")
#         pro_data = ProjectSerializer(pro_data)
#         if not pro_data.data["status"]:
#             return JsonResponse(code="999985", msg="该项目已禁用")
#         try:
#             data = AutomationTestLatelyTenTimeSerializer(
#                 AutomationTaskRunTime.objects.filter(project=project_id).order_by("-startTime")[:10],
#                 many=True).data
#         except IndexError:
#             data = AutomationTestLatelyTenTimeSerializer(
#                 AutomationTaskRunTime.objects.filter(project=project_id).order_by("-startTime"),
#                 many=True).data
#         for i in data:
#             result = AutomationScheduleTestResult.objects.filter(testTime=i["startTime"])
#             _pass = 0
#             fail = 0
#             error = 0
#             for j in result:
#                 if j.result == "PASS":
#                     _pass = _pass + 1
#                 elif j.result == "ERROR":
#                     error = error + 1
#                 elif j.result == "FAIL":
#                     fail = fail + 1
#             total = _pass + error + fail
#             if total:
#                 data[data.index(i)]["fail"] = "%.4f" % (fail / total)
#                 data[data.index(i)]["error"] = "%.4f" % (error / total)
#                 data[data.index(i)]["pass"] = "%.4f" % (1 - fail / total - error / total)
#         data.reverse()
#         return JsonResponse(code="999999", msg="成功！", data=data)

import json
import logging
import platform
import pytz

from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.WriteExcel import Write
from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic, create_json, del_task_crontab
from api_test.common.confighttp import test_api
from api_test.common.schedule_jobs import add_jobs
from api_test.models import Project, AutomationGroupLevelFirst, \
    AutomationTestSchedule, AutomationScheduleApi, AutomationParameter, GlobalHost, AutomationHead, AutomationTestTask, \
    AutomationTestResult, ApiInfo, AutomationParameterRaw, AutomationResponseJson

from api_test.serializers import AutomationGroupLevelFirstSerializer, AutomationTestScheduleSerializer, \
    AutomationScheduleApiSerializer, AutomationScheduleApiListSerializer, AutomationTestTaskSerializer, \
    AutomationTestResultSerializer, ApiInfoSerializer, CorrelationDataSerializer, AutomationTestReportSerializer, \
    AutomationTestScheduleDeserializer, AutomationScheduleApiDeserializer, AutomationHeadDeserializer, \
    AutomationParameterDeserializer, AutomationTestTaskDeserializer, ProjectSerializer, \
    AutomationScheduleDownSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class Group(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取计划分组
        :return:
        """
        project_id = request.GET.get("project_id")
        if not project_id:
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
        obi = AutomationGroupLevelFirst.objects.filter(project=project_id)
        serialize = AutomationGroupLevelFirstSerializer(obi, many=True)
        return JsonResponse(data=serialize.data, code="999999", msg="成功！")


class AddGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["project_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, host
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        新增计划分组
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            obj = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        serializer = AutomationGroupLevelFirstSerializer(data=data)
        if serializer.is_valid():
            serializer.save(project=obj)
        else:
            return JsonResponse(code="999998", msg="失败！")
        record_dynamic(project=serializer.data.get("id"),
                       _type="添加", operationObject="计划分组", user=request.user.pk,
                       data="新增计划分组“%s”" % data["name"])
        return JsonResponse(data={
            "group_id": serializer.data.get("id")
        }, code="999999", msg="成功！")


class DelGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除计划分组名称
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = AutomationGroupLevelFirst.objects.filter(id=data["id"], project=data["project_id"])
        if obi:
            name = obi[0].name
            obi.delete()
        else:
            return JsonResponse(code="999991", msg="分组不存在！")
        record_dynamic(project=data["project_id"],
                       _type="删除", operationObject="计划分组", user=request.user.pk, data="删除计划分组“%s”" % name)
        return JsonResponse(code="999999", msg="成功！")


class UpdateNameGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, host
            if not data["name"]:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改计划分组名称
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationGroupLevelFirst.objects.get(id=data["id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        serializer = AutomationGroupLevelFirstSerializer(data=data)
        if serializer.is_valid():
            serializer.update(instance=obj, validated_data=data)
        else:
            return JsonResponse(code="999998", msg="失败！")
        record_dynamic(project=serializer.data.get("id"),
                       _type="修改", operationObject="计划分组", user=request.user.pk,
                       data="修改计划分组“%s”" % data["name"])
        return JsonResponse(code="999999", msg="成功！")


class UpdateGroup(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["ids"] or not data["automationGroupLevelFirst_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list) \
                    or not isinstance(data["automationGroupLevelFirst_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改计划所属分组
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationGroupLevelFirst.objects.get(id=data["automationGroupLevelFirst_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        id_list = Q()
        for i in data["ids"]:
            id_list = id_list | Q(id=i)
        schedule_list = AutomationTestSchedule.objects.filter(id_list, project=data["project_id"])
        with transaction.atomic():
            schedule_list.update(automationGroupLevelFirst=obj)
            name_list = []
            for j in schedule_list:
                name_list.append(str(j.scheduleName))
            record_dynamic(project=data["project_id"],
                           _type="修改", operationObject="计划", user=request.user.pk, data="修改计划分组，列表“%s”" % name_list)
            return JsonResponse(code="999999", msg="成功！")


class ScheduleList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取计划列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        first_group_id = request.GET.get("first_group_id")
        name = request.GET.get("name")
        if not project_id:
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
        if first_group_id:
            if not first_group_id.isdecimal():
                return JsonResponse(code="999996", msg="参数有误！")
            if name:
                obi = AutomationTestSchedule.objects.filter(project=project_id, scheduleName__contains=name,
                                                        automationGroupLevelFirst=first_group_id).order_by("id")
            else:
                obi = AutomationTestSchedule.objects.filter(project=project_id,
                                                        automationGroupLevelFirst=first_group_id).order_by("id")
        else:
            if name:
                obi = AutomationTestSchedule.objects.filter(project=project_id, scheduleName__contains=name, ).order_by(
                    "id")
            else:
                obi = AutomationTestSchedule.objects.filter(project=project_id).order_by("id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = AutomationTestScheduleSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功！")


class AddSchedule(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["scheduleName"] or not data["automationGroupLevelFirst_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["automationGroupLevelFirst_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        添加计划
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = request.user.pk
        try:
            obj = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        schedule_name = AutomationTestSchedule.objects.filter(scheduleName=data["scheduleName"], project=data["project_id"])
        if len(schedule_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            with transaction.atomic():
                try:
                    serialize = AutomationTestScheduleDeserializer(data=data)
                    if serialize.is_valid():
                        try:
                            if not isinstance(data["automationGroupLevelFirst_id"], int):
                                return JsonResponse(code="999996", msg="参数有误！")
                            obi = AutomationGroupLevelFirst.objects.get(id=data["automationGroupLevelFirst_id"], project=data["project_id"])
                            serialize.save(project=obj, automationGroupLevelFirst=obi, user=User.objects.get(id=data["user"]))
                        except KeyError:
                            serialize.save(project=obj, user=User.objects.get(id=data["user"]))
                        record_dynamic(project=data["project_id"],
                                       _type="新增", operationObject="计划", user=request.user.pk,
                                       data="新增计划\"%s\"" % data["scheduleName"])
                        return JsonResponse(data={"schedule_id": serialize.data.get("id")},
                                            code="999999", msg="成功！")
                    return JsonResponse(code="999996", msg="参数有误！")
                except:
                    return JsonResponse(code="999998", msg="失败！")


class UpdateSchedule(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["scheduleName"] or not data["id"] \
                    or not data["automationGroupLevelFirst_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["id"], int) \
                    or not isinstance(data["automationGroupLevelFirst_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改计划
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationTestSchedule.objects.get(id=data["id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        try:
            AutomationGroupLevelFirst.objects.get(id=data["automationGroupLevelFirst_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999991", msg="分组不存在！")
        schedule_name = AutomationTestSchedule.objects.filter(scheduleName=data["scheduleName"], project=data["project_id"]).exclude(id=data["id"])
        if len(schedule_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serialize = AutomationTestScheduleDeserializer(data=data)
            if serialize.is_valid():
                serialize.update(instance=obj, validated_data=data)
                return JsonResponse(code="999999", msg="成功！")
            return JsonResponse(code="999998", msg="失败！")


class DelSchedule(AddSchedule):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除计划
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        for j in data["ids"]:
            obi = AutomationTestSchedule.objects.filter(id=j, project=data['project_id'])
            if len(obi) != 0:
                name = obi[0].scheduleName
                obi.delete()
                record_dynamic(project=data["project_id"],
                               _type="删除", operationObject="计划", user=request.user.pk, data="删除计划\"%s\"" % name)
        return JsonResponse(code="999999", msg="成功！")


class ApiList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取计划接口列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer！")
        project_id = request.GET.get("project_id")
        schedule_id = request.GET.get("schedule_id")
        if not project_id.isdecimal() or not schedule_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            AutomationTestSchedule.objects.get(id=schedule_id, project=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        data = AutomationScheduleApi.objects.filter(automationTestSchedule=schedule_id).order_by("index")
        paginator = Paginator(data, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = AutomationScheduleApiListSerializer(obm, many=True)
        for i in range(0, len(serialize.data)-1):
            serialize.data[i]["testStatus"] = False
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功！")

class update_api_list_index(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    def post(self,request):
        data = JSONParser().parse(request)
        i=1
        for api in data['apilist']:
            asapi = AutomationScheduleApi.objects.filter(id=api['id'])
            asapi.update(index=i)
            i=i+1

        return JsonResponse(code="999999", msg="成功！")

class ScheduleApiInfo(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取接口详细信息
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        schedule_id = request.GET.get("schedule_id")
        api_id = request.GET.get("api_id")
        if not project_id.isdecimal() or not api_id.isdecimal() or not schedule_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            AutomationTestSchedule.objects.get(id=schedule_id, project=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        try:
            obm = AutomationScheduleApi.objects.get(id=api_id, automationTestSchedule=schedule_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="接口不存在！")
        data = AutomationScheduleApiSerializer(obm).data
        # print(data)
        try:
            name = AutomationResponseJson.objects.get(automationScheduleApi=api_id, type="Regular")
            data["RegularParam"] = name.name
        except ObjectDoesNotExist:
            pass
        return JsonResponse(data=data, code="999999", msg="成功！")


class AddOldApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["schedule_id"] or not data["api_ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or \
                    not isinstance(data["api_ids"], list) or not isinstance(data["schedule_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["api_ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        计划下新增已有的api接口
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationTestSchedule.objects.get(id=data["schedule_id"], project=data["project_id"])

            obj_api = AutomationScheduleApi.objects.filter(automationTestSchedule=data["schedule_id"])
            max_index = len(obj_api)+1

        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        for i in data["api_ids"]:
            try:
                api_data = ApiInfoSerializer(ApiInfo.objects.get(id=i, project=data["project_id"])).data
            except ObjectDoesNotExist:
                continue
            with transaction.atomic():
                api_data["automationTestschedule_id"] = obj.pk

                api_serialize = AutomationScheduleApiDeserializer(data=api_data)
                if api_serialize.is_valid():
                    obk = GlobalHost.objects.get(id=api_data["host"], project=api_data["project"])
                    api_serialize.save(automationTestSchedule=obj, host=obk,index=max_index)
                    schedule_api = api_serialize.data.get("id")
                    if api_data["requestParameterType"] == "form-data":
                        if api_data["requestParameter"]:
                            for j in api_data["requestParameter"]:
                                if j["name"]:
                                    AutomationParameter(automationScheduleApi=AutomationScheduleApi.objects.get(id=schedule_api),
                                                        name=j["name"], value=j["value"], interrelate=False).save()
                    else:
                        if api_data["requestParameterRaw"]:
                            # data = json.loads(serializers.serialize("json",data["requestParameterRaw"]))
                            AutomationParameterRaw(automationScheduleApi=AutomationScheduleApi.objects.get(id=schedule_api),
                                                   data=json.loads(api_data["requestParameterRaw"]["data"])).save()
                    if api_data.get("headers"):
                        for n in api_data["headers"]:
                            if n["name"]:
                                AutomationHead(automationScheduleApi=AutomationScheduleApi.objects.get(id=schedule_api),
                                               name=n["name"], value=n["value"], interrelate=False).save()
                    schedule_name = AutomationTestScheduleSerializer(obj).data["scheduleName"]
                    record_dynamic(project=data["project_id"],
                                   _type="新增", operationObject="计划接口", user=request.user.pk,
                                   data="计划“%s”新增接口\"%s\"" % (schedule_name, api_serialize.data.get("name")))

        return JsonResponse(code="999999", msg="成功！")


class AddNewApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["automationTestSchedule_id"] or not data["apiAddress"] \
                    or not data["requestParameterType"] or not data["examineType"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["automationTestSchedule_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            if data["requestParameterType"] not in ["form-data", "raw", "Restful"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["examineType"] not in ["no_check", "only_check_status", "json", "entirely_check", "Regular_check"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["httpCode"]:
                if data["httpCode"] not in ["200", "404", "400", "502", "500", "302"]:
                    return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data['formatRaw'], bool):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        计划下新增新的api接口
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationTestSchedule.objects.get(id=data["automationTestSchedule_id"], project=data["project_id"])
            obj_api = AutomationScheduleApi.objects.filter(automationTestSchedule=data["automationTestSchedule_id"])
            max_index = len(obj_api) + 1
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        api_name = AutomationScheduleApi.objects.filter(name=data["name"], automationTestSchedule=data["automationTestSchedule_id"])
        if len(api_name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        with transaction.atomic():
            serialize = AutomationScheduleApiDeserializer(data=data)
            obk = GlobalHost.objects.get(id=data["host_id"], project=data["project_id"])
            if serialize.is_valid():
                serialize.save(automationTestSchedule=obj, host=obk,index=max_index)
                api_id = serialize.data.get("id")
                if len(data.get("headDict")):
                    for i in data["headDict"]:
                        if i.get("name"):
                            i["automationScheduleApi_id"] = api_id
                            head_serialize = AutomationHeadDeserializer(data=i)
                            if head_serialize.is_valid():
                                head_serialize.save(automationScheduleApi=AutomationScheduleApi.objects.get(id=api_id))
                if data["requestParameterType"] == "form-data":
                    if len(data.get("requestList")):
                        for i in data["requestList"]:
                            if i.get("name"):
                                i["automationScheduleApi_id"] = api_id
                                param_serialize = AutomationParameterDeserializer(data=i)
                                if param_serialize.is_valid():
                                    param_serialize.save(automationScheduleApi=AutomationScheduleApi.objects.get(id=api_id))
                else:
                    if len(data.get("requestList")):
                        AutomationParameterRaw(automationScheduleApi=AutomationScheduleApi.objects.get(id=api_id),
                                               data=data["requestList"]).save()
                api_ids = AutomationScheduleApi.objects.get(id=api_id)
                if data.get("examineType") == "json":
                    try:
                        response = eval(data["responseData"].replace("true", "True").replace("false", "False").replace("null", "None"))
                        api = "<response[JSON][%s]>" % api_id
                        create_json(api_ids, api, response)
                    except KeyError:
                        return JsonResponse(code="999998", msg="失败！")
                    except AttributeError:
                        return JsonResponse(code="999998", msg="校验内容不能为空！")
                elif data.get("examineType") == 'Regular_check':
                    if data.get("RegularParam"):
                        AutomationResponseJson(automationScheduleApi=api_ids,
                                               name=data["RegularParam"],
                                               tier='<response[Regular][%s]["%s"]' % (api_id, data["responseData"]),
                                               type='Regular').save()
                return JsonResponse(data={"api_id": api_id}, code="999999", msg="成功！")
            return JsonResponse(code="999998", msg="失败！")


class GetCorrelationResponse(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取关联接口数据
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        schedule_id = request.GET.get("schedule_id")
        api_id = request.GET.get("api_id")
        if not project_id.isdecimal() or not schedule_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            AutomationTestSchedule.objects.get(id=schedule_id, project=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        # if api_id:
        #     data = CorrelationDataSerializer(AutomationScheduleApi.objects.filter(automationTestSchedule=schedule_id,
        #                                                                       id__lt=api_id), many=True).data
        # else:
        # a = AutomationScheduleApi.objects.filter(~Q(id=api_id),automationTestSchedule=schedule_id)

        data = CorrelationDataSerializer(AutomationScheduleApi.objects.filter(~Q(id=api_id),automationTestSchedule=schedule_id),
                                             many=True).data
        return JsonResponse(code="999999", msg="成功！", data=data)


class UpdateApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["automationTestSchedule_id"] or not data["name"] or not data["httpType"]\
                    or not data["requestType"] or not data["apiAddress"] or not data["requestParameterType"]\
                    or not data["examineType"] or not data["id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["automationTestSchedule_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            if data["httpType"] not in ["HTTP", "HTTPS"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["requestParameterType"] not in ["form-data", "raw", "Restful"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if data["httpCode"]:
                if data["httpCode"] not in ["200", "404", "400", "502", "500", "302"]:
                    return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data['formatRaw'], bool):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        计划下修改api接口
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obi = AutomationTestSchedule.objects.get(id=data["automationTestSchedule_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        try:
            obj = AutomationScheduleApi.objects.get(id=data["id"], automationTestSchedule=data["automationTestSchedule_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="接口不存在！")
        api_name = AutomationScheduleApi.objects.filter(name=data["name"], automationTestSchedule=data["automationTestSchedule_id"]).exclude(id=data["id"])
        # if not len(api_name):
        #     return JsonResponse(code="999997", msg="存在相同名称！")
        with transaction.atomic():
            serialize = AutomationScheduleApiDeserializer(data=data)
            if serialize.is_valid():
                serialize.update(instance=obj, validated_data=data)
                header = Q()
                if len(data.get("headDict")):
                    for i in data["headDict"]:
                        if i.get("automationScheduleApi") and i.get("id"):
                            header = header | Q(id=i["id"])
                            if i["name"]:
                                head_serialize = AutomationHeadDeserializer(data=i)
                                if head_serialize.is_valid():
                                    i["automationScheduleApi"] = AutomationScheduleApi.objects.get(id=i["automationScheduleApi"])
                                    head_serialize.update(instance=AutomationHead.objects.get(id=i["id"]), validated_data=i)
                        else:
                            if i.get("name"):
                                i["automationScheduleApi"] = data['id']
                                head_serialize = AutomationHeadDeserializer(data=i)
                                if head_serialize.is_valid():
                                    head_serialize.save(automationScheduleApi=AutomationScheduleApi.objects.get(id=data["id"]))
                                    header = header | Q(id=head_serialize.data.get("id"))
                AutomationHead.objects.filter(automationScheduleApi_id=data['id']).exclude(header).delete()
                api_param = Q()
                api_param_raw = Q()
                if len(data.get("requestList")):
                    if data["requestParameterType"] == "form-data":
                        AutomationParameterRaw.objects.filter(automationScheduleApi=data["id"]).delete()
                        for i in data["requestList"]:
                            if i.get("automationScheduleApi") and i.get("id"):
                                api_param = api_param | Q(id=i["id"])
                                if i["name"]:
                                    param_serialize = AutomationParameterDeserializer(data=i)
                                    if param_serialize.is_valid():
                                        i["automationScheduleApi"] = AutomationScheduleApi.objects.get(id=i["automationScheduleApi"])
                                        param_serialize.update(instance=AutomationParameter.objects.get(id=i["id"]),
                                                               validated_data=i)
                            else:
                                if i.get("name"):
                                    i["automationScheduleApi"] = data['id']
                                    param_serialize = AutomationParameterDeserializer(data=i)
                                    if param_serialize.is_valid():
                                        param_serialize.save(automationScheduleApi=AutomationScheduleApi.objects.get(id=data["id"]))
                                        api_param = api_param | Q(id=param_serialize.data.get("id"))
                    else:
                        try:
                            obj = AutomationParameterRaw.objects.get(automationScheduleApi=data["id"])
                            obj.data = data["requestList"]
                            obj.save()
                        except ObjectDoesNotExist:
                            obj = AutomationParameterRaw(automationScheduleApi=AutomationScheduleApi.objects.get(id=data['id']), data=data["requestList"])
                            obj.save()
                        api_param_raw = api_param_raw | Q(id=obj.id)
                AutomationParameter.objects.filter(automationScheduleApi_id=data['id']).exclude(api_param).delete()
                AutomationParameterRaw.objects.filter(automationScheduleApi_id=data['id']).exclude(api_param_raw).delete()
                api_id = AutomationScheduleApi.objects.get(id=data["id"])
                AutomationResponseJson.objects.filter(automationScheduleApi=api_id).delete()

                ##TODO 不同类型参数，需要提前储存路径，如果不选择，手动输入，这里就只需要储存方法，以及参数类型即可，用于关联
                ##这里需要定义好，不同参数类型，取值的格式即可，如：json，可以通过 data.token 类似的格式获取参数
                ##如果是 dubbo类型的如何标注？
                if data.get("examineType") == "json":
                    try:
                        response = ''#eval(data["responseData"].replace("true", "True").replace("false", "False").replace("null", "None"))
                        api = "<response[JSON][%s]>" % api_id
                        create_json(api_id, api, response)
                    except KeyError:
                        return JsonResponse(code="999998", msg="失败！")
                    except AttributeError:
                        return JsonResponse(code="999998", msg="校验内容不能为空！")
                elif data.get("examineType") == 'Regular_check':
                    if data.get("RegularParam"):
                        AutomationResponseJson(automationScheduleApi=api_id,
                                               name=data["RegularParam"],
                                               tier='<response[Regular][%s]["%s"]' % (api_id, data["responseData"]),
                                               type='Regular').save()
                # record_dynamic(project=data["project_id"],
                #                _type="修改", operationObject="计划接口", user=request.user.pk,
                #                data="计划“%s”修改接口\"%s\"" % (obi.scheduleName, data["name"]))
                return JsonResponse(code="999999", msg="成功！")
            return JsonResponse(code="999998", msg="失败！")


class DelApi(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["schedule_id"] or not data["ids"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["schedule_id"], int) \
                    or not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        计划下新增新的api接口
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationTestSchedule.objects.get(id=data["schedule_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        for j in data["ids"]:
            obi = AutomationScheduleApi.objects.filter(id=j, automationTestSchedule=data["schedule_id"])
            if len(obi) != 0:
                name = obi[0].name
                obi.delete()
                record_dynamic(project=data["project_id"],
                               _type="删除", operationObject="计划接口",
                               user=request.user.pk, data="删除计划\"%s\"的接口\"%s\"" % (obj.scheduleName, name))
        return JsonResponse(code="999999", msg="成功！")


class StartTest(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["schedule_id"] or not data["id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int) or not isinstance(data["schedule_id"], int) \
                    or not isinstance(data["id"], int) :
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行测试计划
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obi = AutomationTestSchedule.objects.get(id=data["schedule_id"], project=data["project_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        try:
            obj = AutomationScheduleApi.objects.get(id=data["id"], automationTestSchedule=data["schedule_id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="接口不存在！")
        AutomationTestResult.objects.filter(automationScheduleApi=data["id"]).delete()
        tz = pytz.timezone('Asia/Shanghai')
        start_time = datetime.now(tz)
        format_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            result = test_api(schedule_id=data["schedule_id"],
                              _id=data["id"], project_id=data["project_id"],start_time=format_start_time)
        except Exception as e:
            logging.exception(e)
            return JsonResponse(code="999998", msg="失败！")
        record_dynamic(project=data["project_id"],
                       _type="测试", operationObject="计划接口",
                       user=request.user.pk, data="测试计划“%s”接口\"%s\"" % (obi.scheduleName, obj.name))
        return JsonResponse(data={
            "result": result
        }, code="999999", msg="成功！")


class AddTimeTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"] or not data["name"] or not data["type"] or not data["startTime"] or not data["endTime"] or not data["scheduleId"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int)  or not isinstance(data["scheduleId"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            if data["type"] not in ["circulation", "timing"]:
                return JsonResponse(code="999996", msg="参数有误！")
            try:
                start_time = datetime.strptime(data["startTime"], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(data["endTime"], "%Y-%m-%d %H:%M:%S")
                if start_time > end_time:
                    return JsonResponse(code="999996", msg="参数有误！")
            except ValueError:
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        添加测试任务
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        # print(data['scheduleId'])
        sys_name = platform.system()
        # if sys_name == "Windows" or sys_name == "Darwin":
        #     return JsonResponse(code="999998", msg="该操作只能在Linux系统下进行！")

        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_id = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_id.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_id)
        start_time = data["startTime"]
        end_time = data["endTime"]
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        data["startTime"] = datetime.strptime(data["startTime"], "%Y-%m-%d %H:%M:%S")
        data["endTime"] = datetime.strptime(data["endTime"], "%Y-%m-%d %H:%M:%S")
        schedule_data = AutomationTestSchedule.objects.get(id=data["scheduleId"])
        # try:
        #     host_data = GlobalHost.objects.get(id=data["Host_id"], project=data["project_id"])
        # except ObjectDoesNotExist:
        #     return JsonResponse(code="999992", msg="host不存在！")
        if data["type"] == "circulation":
            if not data["frequency"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["frequency"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            if data["unit"] not in ["m", "h", "d", "w"]:
                return JsonResponse(code="999996", msg="参数有误！")
            task_name = data["name"]
            # if len(task_name):
            #     return JsonResponse(code="999997", msg="存在相同名称！")
            # else:
            try:
                rt = AutomationTestTask.objects.get(Schedule=data["scheduleId"])
                serialize = AutomationTestTaskDeserializer(data=data)
                if serialize.is_valid():
                    serialize.update(instance=rt, validated_data=data)
                    task_id = serialize.data.get("id")
                else:
                    return JsonResponse(code="999996", msg="参数有误！")
            except ObjectDoesNotExist:
                serialize = AutomationTestTaskDeserializer(data=data)
                if serialize.is_valid():
                    serialize.save(project=pro_id)
                    task_id = serialize.data.get("id")
                else:
                    return JsonResponse(code="999996", msg="参数有误！")
            record_dynamic(project=data["scheduleId"],
                           _type="新增", operationObject="任务",
                           user=request.user.pk, data="新增循环任务\"%s\"" % data["name"])
            add_jobs(loop_timing=data["type"],project=str(data["project_id"]),schedule_id=data["scheduleId"],task_name=task_name,start_date=start_time, end_date=end_time, frequency=data["frequency"], unit=data["unit"])
            # add(host_id=data["Host_id"], _type=data["type"], project=str(data["project_id"]),
            #     start_time=start_time, end_time=end_time, frequency=data["frequency"], unit=data["unit"])

        else:
            task_name = data["name"]
            # if len(task_name):
            #     return JsonResponse(code="999997", msg="存在相同名称！")
            # else:
            try:
                rt = AutomationTestTask.objects.get(Schedule=data["scheduleId"])
                serialize = AutomationTestTaskDeserializer(data=data)
                if serialize.is_valid():
                    serialize.update(instance=rt, validated_data=data)
                    task_id = serialize.data.get("id")
                else:
                    return JsonResponse(code="999996", msg="参数有误！")
            except ObjectDoesNotExist:
                serialize = AutomationTestTaskDeserializer(data=data)
                if serialize.is_valid():
                    serialize.save(project=pro_id,Schedule=schedule_data)
                    task_id = serialize.data.get("id")
                else:
                    return JsonResponse(code="999996", msg="参数有误！")
            record_dynamic(project=data["project_id"],
                           _type="新增", operationObject="任务",
                           user=request.user.pk, data="新增定时任务\"%s\"" % data["name"])
            add_jobs(loop_timing=data["type"],project=data["project_id"],schedule_id=data["scheduleId"],task_name=task_name,start_date=start_time, end_date=end_time)
            # add(host_id=data["Host_id"], _type=data["type"], project=str(data["project_id"]),
            #     start_time=start_time, end_time=end_time)
        return JsonResponse(data={"task_id": task_id}, code="999999", msg="成功！")


class GetTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取测试计划执行任务
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        scheduleId = request.GET.get("scheduleId")
        if not project_id.isdecimal() or not scheduleId.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            obj = AutomationTestTaskSerializer(AutomationTestTask.objects.get(Schedule=scheduleId)).data
            return JsonResponse(code="999999", msg="成功！", data=obj)
        except ObjectDoesNotExist:
            return JsonResponse(code="999999", msg="成功！")


class DelTask(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id, id类型为int
            if not data["project_id"]:
                return JsonResponse(code="999996", msg="参数有误！")
            if not isinstance(data["project_id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        执行测试计划
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            pro_data = Project.objects.get(id=data["project_id"])
            if not request.user.is_superuser and pro_data.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obm = AutomationTestTask.objects.filter(project=data["project_id"])
        if obm:
            with transaction.atomic():
                obm.delete()
                del_task_crontab(str(data["project_id"]))
                record_dynamic(project=data["project_id"],
                               _type="删除", operationObject="任务",
                               user=request.user.pk, data="删除任务")
                return JsonResponse(code="999999", msg="成功！")
        else:
            return JsonResponse(code="999986", msg="任务不存在！")


class LookResult(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        查看测试结果详情
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        schedule_id = request.GET.get("schedule_id")
        api_id = request.GET.get("api_id")
        if not project_id.isdecimal() or not api_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            pro_data = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        pro_data = ProjectSerializer(pro_data)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        try:
            AutomationTestSchedule.objects.get(id=schedule_id, project=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999987", msg="计划不存在！")
        try:
            AutomationScheduleApi.objects.get(id=api_id, automationTestSchedule=schedule_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999990", msg="接口不存在！")
        try:
            data = AutomationTestResult.objects.get(automationScheduleApi=api_id)

            serialize = AutomationTestResultSerializer(data)
            serialize.data["responseData"] =serialize.data["responseData"].replace("xa0","")
            # print(serialize.data["responseData"].replace("xa0",""))
            return JsonResponse(data=serialize.data, code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999999", msg="成功！")


class TestReport(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        测试报告
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        schedule_id = request.GET.get("schedule_id")
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
        if obj:
            schedule = Q()
            for i in obj:
                if i.pk ==int(schedule_id):
                    schedule = schedule | Q(automationTestSchedule=i.pk)
            data = AutomationTestReportSerializer(
                AutomationScheduleApi.objects.filter(schedule), many=True).data
            success = 0
            fail = 0
            not_run = 0
            error = 0
            for i in data:

                # i["responseData"] = i["responseData"].replace("xa0","")

                if i["result"] == "PASS":
                    success = success + 1
                elif i["result"] == "FAIL":
                    fail = fail + 1
                elif i["result"] == "ERROR":
                    error = error + 1
                else:
                    not_run = not_run + 1
            return JsonResponse(code="999999", msg="成功！", data={"data": data,
                                                                "total": len(data),
                                                                "pass": success,
                                                                "fail": fail,
                                                                "error": error,
                                                                "NotRun": not_run
                                                                })
        else:
            return JsonResponse(code="999987", msg="计划不存在！")


class DownLoadSchedule(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取计划下载文档路径
        :param request:
        :return:
        """
        project_id = request.GET.get("project_id")
        try:
            if not project_id.isdecimal():
                return JsonResponse(code="999996", msg="参数有误!")
        except AttributeError:
            return JsonResponse(code="999996", msg="参数有误！")
        try:
            obj = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在!")
        pro_data = ProjectSerializer(obj)
        if not pro_data.data["status"]:
            return JsonResponse(code="999985", msg="该项目已禁用")
        obi = AutomationGroupLevelFirst.objects.filter(project=project_id).order_by("id")
        data = AutomationScheduleDownSerializer(obi, many=True).data
        path = "./api_test/ApiDoc/%s.xlsx" % str(obj.name)
        result = Write(path).write_schedule(data)
        if result:
            return JsonResponse(code="999999", msg="成功！", data=path)
        else:
            return JsonResponse(code="999998", msg="失败")


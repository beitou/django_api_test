import logging

from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.utils import json

from api_test.common.api_response import JsonResponse
from api_test.serializers import ScriptDeserializer, ScriptSerializer, ScriptFileSerializer, ScriptFileDeserializer, \
    ScriptParameterSerializer, ScriptParameterDeserializer
from api_test.models import Script, ScriptFile, ScriptParameter

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class ScriptList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取脚本列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        if name:
            obi = Script.objects.filter(name__contains=name, status="1").order_by("id")
        else:
            obi = Script.objects.filter(status="1").order_by("id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = ScriptSerializer(obm, many=True)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功")


class AddScript(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, version, type
            if not data["name"] or not data["type"]:
                return JsonResponse(code="999996", msg="参数有误！")
            # type 类型 Web， App
            # if data["type"] not in ["Web", "App"]:
            #     return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    # def add_project_member(self, project, user):
    #     """
    #     添加项目创建人员
    #     :param project: 项目ID
    #     :param user:  用户ID
    #     :return:
    #     """
    #     member_serializer = ProjectMemberDeserializer(data={
    #         "permissionType": "超级管理员", "project": project,
    #         "user": user
    #     })
    #     project = Project.objects.get(id=project)
    #     user = User.objects.get(id=user)
    #     if member_serializer.is_valid():
    #         member_serializer.save(project=project, user=user)

    def post(self, request):
        """
        新增项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = request.user.pk
        data["status"] = "1"
        script_Deserializer = ScriptDeserializer(data=data)
        try:
            Script.objects.get(name=data["name"])

            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if script_Deserializer.is_valid():
                    # 保持新项目
                    script_Deserializer.save()
                    # 记录动态
                    # record_dynamic(project=project_serializer.data.get("id"),
                    #                _type="添加", operationObject="项目", user=request.user.pk, data=data["name"])
                    # 创建项目的用户添加为该项目的成员
                    # self.add_project_member(project_serializer.data.get("id"), request.user.pk)
                    return JsonResponse(data={
                        "project_id": script_Deserializer.data.get("id")
                    }, code="999999", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")


class DelScript(APIView):
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
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                try:
                    obj = Script.objects.get(id=i)
                    if not request.user.is_superuser and obj.user.is_superuser:
                        return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="项目不存在！")
            for j in data["ids"]:
                obj = Script.objects.filter(id=j)
                obj.update(status='0')

                # my_user_cron = CronTab(user=True)
                # my_user_cron.remove_all(comment=j)
                # my_user_cron.write()
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


class UpdateScript(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        data = JSONParser().parse(request)

        with transaction.atomic():
            # 4。 保存在线编辑文件
            if data['editFile'] != "" and data['fileDetail'] != '':
                sfileEdit = ScriptFile.objects.filter(fileName=data['editFile'], sid=data['script_id'], status='1')
                if sfileEdit:
                    sfileEdit.update(fileDetail=data['fileDetail'])
                else:
                    scriptfile = {}
                    scriptfile["sid"] = data.get("script_id")
                    scriptfile["fileName"] = data['editFile']
                    scriptfile["fileDetail"] = data['fileDetail']
                    scriptfile["user"] = request.user.pk
                    scriptFileDeserializer = ScriptFileDeserializer(data=scriptfile)
                    if scriptFileDeserializer.is_valid():
                        scriptFileDeserializer.save()
            # 1. 设置文件入口函数
            sfile = ScriptFile.objects.filter(sid=data["script_id"], status='1')
            if sfile.count() == 1:
                sfile.update(executable=1)
            else:
                sfile.update(executable=0)
                sfile_executable = ScriptFile.objects.filter(fileName=data["executable"])
                sfile_executable.update(executable=1)
            # # 2. 保存脚本名称和描述
            script = Script.objects.filter(id=data["script_id"])
            if script.count() == 0:
                return JsonResponse(code="999998", msg="未找到项目")
            script.update(name=data["name"], description=data["description"])
            # # 3。保存脚本参数
            spobj_del = ScriptParameter.objects.filter(sid=data["script_id"])
            spobj_del.delete()
            scriptParams = data["scriptParams"]
            scriptp = {}
            scriptp['sid'] = data["script_id"]
            for sp in scriptParams:
                if sp.get("name") != "":
                    scriptp['name'] = sp.get("name")
                    scriptp['value'] = sp.get("value")
                    scriptp['description'] = sp.get("description")
                    spobj = ScriptParameter.objects.filter(sid=scriptp['sid'], name=scriptp['name'])
                    if spobj:
                        spobj.update(value=scriptp['value'])
                    else:
                        scriptParamsDeserializer = ScriptParameterDeserializer(data=scriptp)
                        if scriptParamsDeserializer.is_valid():
                            scriptParamsDeserializer.save()

        return JsonResponse(code="999999", msg="保存成功")


class GetScript(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目详情
        :param request:
        :return:
        """
        script_id = request.GET.get("script_id")
        if not script_id:
            return JsonResponse(code="999996", msg="参数有误！")
        if not script_id.isdecimal():
            return JsonResponse(code="999996", msg="参数有误！")
        scriptFiles = ScriptFile.objects.filter(sid=script_id, status='1')
        # fileList=[]
        # for sf in scriptFiles:
        #     fileList.append(ScriptFileSerializer(sf))
        try:
            obj = Script.objects.get(id=script_id, status='1')
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        serialize = ScriptSerializer(obj)
        sfSer = ScriptFileSerializer(scriptFiles, many=True)
        # print(sfSer.data)
        spobj = ScriptParameter.objects.filter(sid=script_id)
        temp = [{'name': '', 'value': ''}]
        for sp in spobj:
            p = {'name': sp.name, 'value': sp.value, 'description': sp.description}
            temp.append(p)

        if serialize.data["status"]:
            return JsonResponse(data={
                'name': serialize.data["name"],
                'description': serialize.data["description"],
                'fileList': sfSer.data,
                'parameter': temp,

            }, code="999999", msg="成功！")
        else:
            return JsonResponse(code="999985", msg="该项目已禁用")


class AddRunResult(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        return ""


class AddHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def post(self, request):
        return ""


class HistoryList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        return ""

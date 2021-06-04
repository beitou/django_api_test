from django.contrib.auth.models import User
from rest_framework import serializers, fields
from rest_framework.authtoken.models import Token

from api_test.models import Project, ProjectDynamic, ProjectMember, GlobalHost, ApiGroupLevelFirst, \
    ApiInfo, APIRequestHistory, ApiOperationHistory, AutomationGroupLevelFirst, \
    AutomationTestSchedule, AutomationScheduleApi, AutomationHead, AutomationParameter, AutomationTestTask, \
    AutomationTestResult, ApiHead, ApiParameter, ApiResponse, ApiParameterRaw, AutomationParameterRaw, \
    AutomationResponseJson, AutomationTaskRunTime, AutomationScheduleTestResult, AutomationReportSendConfig, \
    CaseProject, CaseProjectDynamic, CaseProjectMember, CaseRequirement, CaseInfo, CaseReportSendConfig, \
    CaseOperationHistory, Stage,Script,ScriptFile,ScriptParameter,ScriptGroup


class TokenSerializer(serializers.ModelSerializer):
    """
    用户信息序列化
    """
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.user.phone")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.CharField(source="user.date_joined")
    userphoto = serializers.CharField(source="user.user.userphoto")

    class Meta:
        model = Token
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'key', 'date_joined','userphoto')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class ProjectDeserializer(serializers.ModelSerializer):
    """
    项目信息反序列化
    """
    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'description', 'user')




class ScriptDeserializer(serializers.ModelSerializer):
    """
    脚本信息反序列化
    """
    class Meta:
        model = Script
        fields = ('name','description','status','user')

class ScriptSerializer(serializers.ModelSerializer):
    '''
    脚本信息序列化
    '''
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Script
        fields = ('id','name','description','scriptGroup','status','createTime','LastUpdateTime','user')


class ScriptFileDeserializer(serializers.ModelSerializer):
    '''
    脚本文件反序列化
    '''
    class Meta:
         model = ScriptFile
         fields = ('sid', 'fileName', 'fileDetail', 'status','executable','user')

class ScriptFileSerializer(serializers.ModelSerializer):
    '''
    脚本文件序列化
    '''

    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')
    class Meta:
         model = ScriptFile
         fields = ('id','sid', 'fileName', 'fileDetail', 'status','executable','createTime','LastUpdateTime','user')

class ScriptParameterSerializer(serializers.ModelSerializer):
    '''
    脚本参数序列化
    '''

    class Meta:
         model = ScriptParameter
         fields = ('id','sid', 'name', 'value', 'description','status')

class ScriptParameterDeserializer(serializers.ModelSerializer):
    '''
    脚本参数反序列化
    '''
    class Meta:
         model = ScriptParameter
         fields = ('sid', 'name', 'value','description', 'status')

class ScriptGroupSerializer(serializers.ModelSerializer):
    '''
        脚本分类序列化
        '''

    class Meta:
        model = ScriptGroup
        fields = ('id', 'name', 'status')

class ScriptGroupDeserializer(serializers.ModelSerializer):
    '''
        脚本分类反序列化
        '''

    class Meta:
        model = ScriptGroup
        fields = ('id', 'name', 'status')

class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    apiCount = serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    scheduleApiCount = serializers.SerializerMethodField()
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'apiCount',
                  'dynamicCount', 'memberCount', 'description', 'user', 'scheduleApiCount')

    def get_apiCount(self, obj):
        return obj.api_project.all().count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()

    def get_scheduleApiCount(self, obj):
        a = 0
        for obk in obj.schedule_api.all(): a += obk.api.all().count()
        return a


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """
    class Meta:
        model = ProjectDynamic
        fields = ('id', 'project', 'time', 'type', 'operationObject', 'user', 'description')


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.CharField(source='user.username')
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'time', 'type', 'operationObject', 'operationUser', 'description')


class ProjectMemberDeserializer(serializers.ModelSerializer):
    """
    项目成员信息反序列化
    """
    class Meta:
        model = ProjectMember
        fields = ('id', 'permissionType', 'project', 'user')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    项目成员信息序列化
    """
    username = serializers.CharField(source='user.username')
    userPhone = serializers.CharField(source='user.user.phone')
    userEmail = serializers.CharField(source='user.email')

    class Meta:
        model = ProjectMember
        fields = ('id', 'permissionType', 'username', 'userPhone', 'userEmail')


class GlobalHostSerializer(serializers.ModelSerializer):
    """
    host信息序列化
    """

    class Meta:
        model = GlobalHost
        fields = ('id', 'project_id', 'name', 'host', 'status', 'description')


class ApiGroupLevelFirstSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """
    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class ApiGroupLevelFirstDeserializer(serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """
    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class ApiHeadSerializer(serializers.ModelSerializer):
    """
    接口请求头序列化
    """
    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiHeadDeserializer(serializers.ModelSerializer):
    """
    接口请求头反序列化
    """

    class Meta:
        model = ApiHead
        fields = ('id', 'api', 'name', 'value')


class ApiParameterSerializer(serializers.ModelSerializer):
    """
    接口请求参数序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterDeserializer(serializers.ModelSerializer):
    """
    接口请求参数反序列化
    """

    class Meta:
        model = ApiParameter
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'restrict', 'description')


class ApiParameterRawSerializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiParameterRawDeserializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """

    class Meta:
        model = ApiParameterRaw
        fields = ('id', 'api', 'data')


class ApiResponseSerializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiResponseDeserializer(serializers.ModelSerializer):
    """
    接口返回参数序列化
    """

    class Meta:
        model = ApiResponse
        fields = ('id', 'api', 'name', 'value', '_type', 'required', 'description')


class ApiInfoSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    headers = ApiHeadSerializer(many=True, read_only=True)
    requestParameter = ApiParameterSerializer(many=True, read_only=True)
    response = ApiResponseSerializer(many=True, read_only=True)
    requestParameterRaw = ApiParameterRawSerializer(many=False, read_only=True)
    hostName = serializers.CharField(source='host.host')
    userUpdate = serializers.CharField(source='userUpdate.username')

    class Meta:
        model = ApiInfo
        fields = ('id', 'apiGroupLevelFirst', 'project', 'name', 'httpType', 'requestType', 'apiAddress', 'dubboMethod', 'host', 'headers',
                  'requestParameterType', 'requestParameter', 'requestParameterRaw', 'status', 'hostName',
                  'response', 'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description')


class ApiInfoDeserializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    class Meta:
        model = ApiInfo
        fields = ('id', 'project_id', 'name', 'httpType',
                  'requestType', 'apiAddress', 'host_id', 'requestParameterType', 'status',
                  'mockCode', 'data', 'lastUpdateTime', 'userUpdate', 'description', 'dubboMethod')


class ApiInfoDocSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    First = ApiInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ApiGroupLevelFirst
        fields = ('id', 'name', 'First')


class ApiInfoListSerializer(serializers.ModelSerializer):
    """
    接口信息序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.username')

    class Meta:
        model = ApiInfo
        fields = ('id', 'name', 'requestType', 'apiAddress', 'mockStatus', 'lastUpdateTime', 'userUpdate')


class APIRequestHistorySerializer(serializers.ModelSerializer):
    """
    接口请求历史信息序列化
    """
    requestTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = APIRequestHistory
        fields = ('id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class APIRequestHistoryDeserializer(serializers.ModelSerializer):
    """
    接口请求历史信息反序列化
    """
    class Meta:
        model = APIRequestHistory
        fields = ('id', 'api_id', 'requestTime', 'requestType', 'requestAddress', 'httpCode')


class ApiOperationHistorySerializer(serializers.ModelSerializer):
    """
    接口操作历史信息序列化
    """
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'user', 'time', 'description')


class ApiOperationHistoryDeserializer(serializers.ModelSerializer):
    """
    接口操作历史信息反序列化
    """

    class Meta:
        model = ApiOperationHistory
        fields = ('id', 'apiInfo', 'user', 'time', 'description')


class AutomationGroupLevelFirstSerializer(serializers.ModelSerializer):
    """
    自动化计划一级分组信息序列化
    """
    class Meta:
        model = AutomationGroupLevelFirst
        fields = ('id', 'project_id', 'name')


class AutomationTestScheduleSerializer(serializers.ModelSerializer):
    """
    自动化计划信息序列化
    """
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createUser = serializers.CharField(source='user.username')
    api_count = serializers.SerializerMethodField()

    class Meta:
        model = AutomationTestSchedule
        fields = ('id', 'automationGroupLevelFirst', 'scheduleName', 'createUser',
                  'description', 'updateTime','api_count')
    def get_api_count(self,obj):
        return obj.api.all().count()


class AutomationTestScheduleDeserializer(serializers.ModelSerializer):
    """
    自动化计划信息反序列化
    """
    class Meta:
        model = AutomationTestSchedule
        fields = ('id', 'project_id', 'automationGroupLevelFirst', 'scheduleName', 'user',
                  'description', 'updateTime')


class AutomationHeadSerializer(serializers.ModelSerializer):
    """
    自动化计划接口请求头信息序列化
    """
    class Meta:
        model = AutomationHead
        fields = ('id', 'automationScheduleApi', 'name', 'value', 'interrelate')


class AutomationHeadDeserializer(serializers.ModelSerializer):
    """
    自动化计划接口请求头信息反序列化
    """
    class Meta:
        model = AutomationHead
        fields = ('id', 'automationScheduleApi_id', 'name', 'value', 'interrelate')


class AutomationParameterSerializer(serializers.ModelSerializer):
    """
    自动化计划接口请求参数信息序列化
    """
    class Meta:
        model = AutomationParameter
        fields = ('id', 'automationScheduleApi', 'name', 'value', 'interrelate')


class AutomationParameterDeserializer(serializers.ModelSerializer):
    """
    自动化计划接口请求参数信息反序列化
    """
    class Meta:
        model = AutomationParameter
        fields = ('id', 'automationScheduleApi_id', 'name', 'value', 'interrelate')


class AutomationParameterRawSerializer(serializers.ModelSerializer):
    """
    接口请求参数源数据序列化
    """
    class Meta:
        model = AutomationParameterRaw
        fields = ('id', 'automationScheduleApi', 'data')


class AutomationParameterRawDeserializer(serializers.ModelSerializer):
    """
    接口请求参数源数据反序列化
    """
    class Meta:
        model = AutomationParameterRaw
        fields = ('id', 'automationScheduleApi_id', 'data')


class AutomationResponseJsonSerializer(serializers.ModelSerializer):
    """
    返回JSON参数序列化
    """

    class Meta:
        model = AutomationResponseJson
        fields = ('id', 'automationScheduleApi', 'name', 'tier')


class AutomationResponseJsonDeserializer(serializers.ModelSerializer):
    """
    返回JSON参数反序列化
    """

    class Meta:
        model = AutomationResponseJson
        fields = ('id', 'automationScheduleApi', 'name', 'tier')

class AutomationTestResultSerializer(serializers.ModelSerializer):
    """
    手动测试结果详情序列化
    """
    testTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = AutomationTestResult
        fields = ('id', 'url', 'requestType', 'header', 'parameter', 'statusCode', 'examineType', 'data',
                  'result', 'httpStatus', 'responseData', 'testTime')

class CorrelationDataSerializer(serializers.ModelSerializer):
    """
    关联数据序列化
    """
    test_result = AutomationTestResultSerializer(many=False)

    class Meta:
        model = AutomationScheduleApi
        fields = ("id", "name","test_result")


class AutomationScheduleApiSerializer(serializers.ModelSerializer):
    """
    自动化计划接口详细信息序列化
    """
    header = AutomationHeadSerializer(many=True, read_only=True)
    parameterList = AutomationParameterSerializer(many=True, read_only=True)
    parameterRaw = AutomationParameterRawSerializer(many=False, read_only=True)
    hostName = serializers.CharField(source='host.host')
    apiCount = serializers.SerializerMethodField()

    class Meta:
        model = AutomationScheduleApi
        fields = ('id', 'name', 'httpType', 'requestType', 'apiAddress', 'header', 'requestParameterType', 'formatRaw',
                  'parameterList', 'parameterRaw', 'examineType', 'httpCode', 'responseData', 'hostName', 'host_id', 'dubboMethod','apiCount')
    def get_apiCount(self, obj):
        return obj.auto_result.all().count()

class AutomationScheduleDownloadSerializer(serializers.ModelSerializer):
    """
    下载计划读取数据序列
    """
    # api = AutomationScheduleApiSerializer(many=True, read_only=True)
    updateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # automationGroupLevelFirst = serializers.CharField(source='automationGroupLevelFirst.name')
    user = serializers.CharField(source="user.username")
    api = serializers.SerializerMethodField()

    class Meta:
        model = AutomationTestSchedule
        fields = ('scheduleName', 'user', 'updateTime', 'api')

    def get_api(self, obj):
        return AutomationScheduleApiSerializer(
            AutomationScheduleApi.objects.filter(automationTestSchedule=obj).order_by("id"),
            many=True
        ).data


class AutomationScheduleDownSerializer(serializers.ModelSerializer):
    """
    下载计划读取数据序列
    """
    automationGroup = AutomationScheduleDownloadSerializer(many=True, read_only=True)

    class Meta:
        model = AutomationGroupLevelFirst
        fields = ("name", "automationGroup")


class AutomationScheduleApiDeserializer(serializers.ModelSerializer):
    """
    自动化计划接口详细信息反序列化
    """
    class Meta:
        model = AutomationScheduleApi
        fields = ('id', 'automationTestSchedule_id', 'host_id', 'name', 'requestType', 'httpType', 'apiAddress', 'requestParameterType',
                  'formatRaw', 'examineType', 'httpCode', 'responseData', 'dubboMethod','index')


class AutomationScheduleApiListSerializer(serializers.ModelSerializer):
    """
    自动化计划接口列表信息序列化
    """

    class Meta:
        model = AutomationScheduleApi
        fields = ('id', 'name',  'apiAddress','index')


class AutomationTestTaskSerializer(serializers.ModelSerializer):
    """
    定时任务信息序列化
    """
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    endTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = AutomationTestTask
        fields = ('id', 'project','Schedule', 'name', 'type', 'frequency', 'unit', 'startTime', 'endTime')


class AutomationTestTaskDeserializer(serializers.ModelSerializer):
    """
    定时任务信息反序列化
    """

    class Meta:
        model = AutomationTestTask
        fields = ('id', 'project_id', 'Schedule_id', 'name', 'type', 'frequency', 'unit', 'startTime', 'endTime')


class AutomationTestReportSerializer(serializers.ModelSerializer):
    """
    测试报告测试结果信息序列化
    """
    result = serializers.CharField(source='test_result.result')
    host = serializers.CharField(source='test_result.host')
    parameter = serializers.CharField(source='test_result.parameter')
    httpStatus = serializers.CharField(source='test_result.httpStatus')
    responseData = serializers.CharField(source='test_result.responseData')
    automationTestSchedule = serializers.CharField(source='automationTestSchedule.scheduleName')
    testTime = serializers.CharField(source='test_result.testTime')
    hostName = serializers.CharField(source='host.host')

    class Meta:
        model = AutomationScheduleApi
        fields = ('id', 'automationTestSchedule', 'name', 'host', 'httpType', 'requestType', 'apiAddress', 'examineType',
                  'result', 'parameter', 'httpStatus', 'responseData', 'testTime', 'dubboMethod', 'host', 'hostName')


class AutomationTaskRunTimeSerializer(serializers.ModelSerializer):
    """
    任务执行时间
    """
    startTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    project = serializers.CharField(source='project.name')
    Schedule_name = serializers.CharField(source='Schedule.scheduleName')
    Schedule_id = serializers.CharField(source='Schedule.id')


    class Meta:
        model = AutomationTaskRunTime
        fields = ('id', 'project', 'startTime', 'elapsedTime', 'host','Schedule','result','Schedule_name','Schedule_id')





class AutomationAutoTestResultSerializer(serializers.ModelSerializer):
    """
    自动测试结果详情序列化
    """

    name = serializers.CharField(source='automationScheduleApi.name')
    httpType = serializers.CharField(source='automationScheduleApi.httpType')
    requestType = serializers.CharField(source='automationScheduleApi.requestType')
    apiAddress = serializers.CharField(source='automationScheduleApi.apiAddress')
    examineType = serializers.CharField(source='automationScheduleApi.examineType')
    automationTestSchedule = serializers.CharField(source='automationScheduleApi.automationTestSchedule')

    # hostName = serializers.CharField(source='host.host')

    class Meta:
        model = AutomationScheduleTestResult
        fields = ('id', 'automationTestSchedule', 'name', 'httpType', 'header', 'requestType', 'apiAddress', 'examineType',
                  'result', 'parameter', 'httpStatus', 'responseHeader', 'responseData', 'testTime')




class AutomationTestLatelyTenTimeSerializer(serializers.ModelSerializer):
    """
    最近10次测试结果
    """
    class Meta:
        model = AutomationTaskRunTime
        fields = ("id", "startTime")


class AutomationReportSendConfigSerializer(serializers.ModelSerializer):
    """
    发送人配置序列
    """
    project = serializers.CharField(source='project.name')

    class Meta:
        model = AutomationReportSendConfig
        fields = ("id", "project", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')


class AutomationReportSendConfigDeserializer(serializers.ModelSerializer):
    """
    发送人配置反序列
    """

    class Meta:
        model = AutomationReportSendConfig
        fields = ("id", "project_id", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')

class CaseReportSendConfigSerializer(serializers.ModelSerializer):
    """
    发送人配置序列
    """
    caseProject = serializers.CharField(source='caseProject.name')

    class Meta:
        model = CaseReportSendConfig
        fields = ("id", "caseProject", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')


class CaseReportSendConfigDeserializer(serializers.ModelSerializer):
    """
    发送人配置反序列
    """

    class Meta:
        model = CaseReportSendConfig
        fields = ("id", "caseProject_id", 'reportFrom', 'mailUser', 'mailPass', 'mailSmtp')



class CaseProjectDeserializer(serializers.ModelSerializer):
    """
    项目信息反序列化
    """
    class Meta:
        model = CaseProject
        fields = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'description', 'user', 'yn')


class CaseProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    caseCount = serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    requirementCount = serializers.SerializerMethodField()
    LastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = CaseProject
        fields = ('id', 'name', 'version', 'type', 'status', 'LastUpdateTime', 'createTime', 'yn', 'caseCount',
                  'dynamicCount', 'memberCount', 'requirementCount', 'description', 'user')

    def get_caseCount(self, obj):
        return obj.case_project.filter(yn=0).count()

    def get_requirementCount(self, obj):
        return obj.project_requirement.filter(yn=0).count()

    def get_dynamicCount(self, obj):
        return obj.dynamic_case_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_case_project.all().count()



class CaseProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """
    class Meta:
        model = CaseProjectDynamic
        fields = ('id', 'caseProject', 'time', 'type', 'operationObject', 'user', 'description')


class CaseProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.CharField(source='user.username')
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = CaseProjectDynamic
        fields = ('id', 'time', 'type', 'operationObject', 'operationUser', 'description')


class CaseProjectMemberDeserializer(serializers.ModelSerializer):
    """
    项目成员信息反序列化
    """
    class Meta:
        model = CaseProjectMember
        fields = ('id', 'permissionType', 'caseProject', 'user')


class CaseProjectMemberSerializer(serializers.ModelSerializer):
    """
    项目成员信息序列化
    """
    username = serializers.CharField(source='user.username')
    userPhone = serializers.CharField(source='user.user.phone')
    userEmail = serializers.CharField(source='user.email')

    class Meta:
        model = CaseProjectMember
        fields = ('id', 'permissionType', 'username', 'userPhone', 'userEmail')


class CaseRequirementSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """
    caseRequirementCount = serializers.SerializerMethodField()
    casePassCount = serializers.SerializerMethodField()
    caseFailCount = serializers.SerializerMethodField()
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = CaseRequirement
        fields = ('id', 'caseProject', 'name', 'user', 'createTime', 'yn', 'caseRequirementCount', 'caseFailCount',
                  'casePassCount', 'zentao_id')

    def get_caseRequirementCount(self, obj):
        return obj.case_requirement.filter(yn=0).count()

    def get_casePassCount(self, obj):
        return obj.case_requirement.filter(actualResult=1, yn=0).count()

    def get_caseFailCount(self, obj):
        return obj.case_requirement.filter(actualResult=2, yn=0).count()


class CaseRequirementDeserializer(serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """
    class Meta:
        model = CaseRequirement
        fields = ('id', 'caseProject_id', 'name', 'user', 'createTime', 'zentao_id', 'yn')


class CaseSerializer(serializers.ModelSerializer):
    """
    用例序列化
    """
    lastUpdateTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    createTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    userUpdate = serializers.CharField(source='userUpdate.username')

    class Meta:
        model = CaseInfo
        field = ('id', 'caseProject', 'caseRequirement', 'name', 'priority', 'testType', 'testTontent', 'operationSteps',
                 'stage', 'expectedResults', 'actualResult', 'reason', 'createTime', 'lastUpdateTime', 'version',
                 'hardware', 'userUpdate', 'yn')
        fields = "__all__"


class CaseDeserializer(serializers.ModelSerializer):
    """
    用例序列化
    """
    stage = fields.MultipleChoiceField(choices=Stage)

    class Meta:
        model = CaseInfo
        field = ('id', 'caseProject_id', 'caseRequirement_id', 'name', 'priority', 'testType', 'testTontent',
                 'stage', 'operationSteps', 'expectedResults', 'actualResult', 'reason', 'createTime', 'lastUpdateTime',
                 'version', 'hardware', 'userUpdate', 'yn')
        fields = "__all__"


class CaseOperationHistorySerializer(serializers.ModelSerializer):
    """
    用例记录序列化
    """
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    user = serializers.CharField(source='user.username')

    class Meta:
        model = CaseOperationHistory
        fields = "__all__"






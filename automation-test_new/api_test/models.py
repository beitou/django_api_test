from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from multiselectfield import MultiSelectField

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE'),
    ('DUBBO', 'DUBBO')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('Restful', 'Restful')
)

PARAMETER_TYPE_CHOICE = (
    ('text', 'text'),
    ('file', 'file')
)

HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)

EXAMINE_TYPE_CHOICE = (
    ('no_check', '不校验'),
    ('only_check_status', '校验http状态'),
    ('json', 'JSON校验'),
    ('entirely_check', '完全校验'),
    ('Regular_check', '正则校验'),
    ('Schema_check', 'Schema校验'),
)

UNIT_CHOICE = (
    ('m', '分'),
    ('h', '时'),
    ('d', '天'),
    ('w', '周'),
)

RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
)


TASK_CHOICE = (
    ('circulation', '循环'),
    ('timing', '定时'),
)
STATUS_CHOICE=(
    ('0','废弃'),
    ('1','使用中'),
)

Stage = (
        ('0', '冒烟'),
        ('1', '功能'),
        ('2', '回归'),
    )

#post_save                   # django的modal对象保存后，自动触发
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# ==================扩展用户====================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='user')
    phone = models.CharField(max_length=11, default='', blank=True, verbose_name='手机号')
    userphoto = models.CharField(max_length=100,default='',blank=True,verbose_name='用户头像')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.phone


class Project(models.Model):
    """
    项目表
    """
    ProjectType = (
        ('Web', 'Web'),
        ('App', 'App')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='项目名称')
    version = models.CharField(max_length=50, verbose_name='版本')
    type = models.CharField(max_length=50, verbose_name='类型', choices=ProjectType)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='dynamic_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(max_length=128, verbose_name='操作时间')
    type = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, related_name='userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True,  verbose_name='描述')

    def __unicode__(self):
        return self.type

    def __str__(self):
        return str(self.time)

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'


class ProjectMember(models.Model):
    """
    项目成员
    """
    CHOICES = (
        ('超级管理员', '超级管理员'),
        ('开发人员', '开发人员'),
        ('测试人员', '测试人员')
    )
    id = models.AutoField(primary_key=True)
    permissionType = models.CharField(max_length=50, verbose_name='权限角色', choices=CHOICES)
    project = models.ForeignKey(Project, related_name='member_project', on_delete=models.CASCADE, verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.permissionType

    def __str__(self):
        return self.permissionType

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'


class GlobalHost(models.Model):
    """
    host域名
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=1024, verbose_name='Host地址')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HOST'
        verbose_name_plural = 'HOST管理'


class CustomMethod(models.Model):
    """
    自定义方法
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='方法名')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    type = models.CharField(max_length=50, verbose_name='类型')
    dataCode = models.TextField(verbose_name='代码')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '自定义方法'
        verbose_name_plural = '自定义方法'


class ApiGroupLevelFirst(models.Model):
    """
    接口一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='接口一级分组名称')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'


class ApiInfo(models.Model):
    """
    接口信息
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='api_project', on_delete=models.CASCADE, verbose_name='所属项目')
    apiGroupLevelFirst = models.ForeignKey(ApiGroupLevelFirst, blank=True, null=True,
                                           related_name='First',
                                           on_delete=models.SET_NULL, verbose_name='所属一级分组')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.ForeignKey(GlobalHost, on_delete=models.DO_NOTHING, verbose_name='所属host')
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    dubboMethod = models.CharField(max_length=1024, blank=True, null=True, verbose_name='DUBBO方法')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.BooleanField(default=True, verbose_name='状态')
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")
    mockCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    data = models.TextField(blank=True, null=True, verbose_name='mock内容')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='更新人',
                                   related_name='ApiUpdateUser')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'


class ApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='headers')
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


class ApiParameter(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameter')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型', choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必填")
    restrict = models.CharField(max_length=1024, blank=True, null=True, verbose_name="输入限制")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求参数'
        verbose_name_plural = '请求参数管理'


class ApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.OneToOneField(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameterRaw')
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'


class ApiResponse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='response')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型', choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必含")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '返回参数'
        verbose_name_plural = '返回参数管理'


class APIRequestHistory(models.Model):
    """
    接口请求历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    requestTime = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')
    requestType = models.CharField(max_length=50, verbose_name='请求方法')
    requestAddress = models.CharField(max_length=1024, verbose_name='请求地址')
    httpCode = models.CharField(max_length=50, verbose_name='HTTP状态')

    def __unicode__(self):
        return self.requestAddress

    class Meta:
        verbose_name = '接口请求历史'
        verbose_name_plural = '接口请求历史'


class ApiOperationHistory(models.Model):
    """
    API操作历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='用户姓名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='操作内容')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = '接口操作历史'
        verbose_name_plural = '接口操作历史'


class AutomationGroupLevelFirst(models.Model):
    """
    自动化计划一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='计划一级分组')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划分组'
        verbose_name_plural = '计划分组管理'


class AutomationTestSchedule(models.Model):
    """
    自动化测试用例
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目', related_name="schedule_api")
    automationGroupLevelFirst = models.ForeignKey(AutomationGroupLevelFirst, blank=True, null=True,
                                                  on_delete=models.SET_NULL, verbose_name='所属计划一级分组', related_name="automationGroup")
    # automationGroupLevelSecond = models.ForeignKey(AutomationGroupLevelSecond, blank=True, null=True,
    #                                                on_delete=models.SET_NULL, verbose_name='所属计划二级分组')
    scheduleName = models.CharField(max_length=50, verbose_name='计划名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="创建人",
                             related_name="createUser")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.scheduleName

    def __str__(self):
        return self.scheduleName

    class Meta:
        verbose_name = '自动化测试用例'
        verbose_name_plural = '自动化测试用例'


class AutomationScheduleApi(models.Model):
    """
    计划执行接口
    """
    id = models.AutoField(primary_key=True)
    automationTestSchedule = models.ForeignKey(AutomationTestSchedule, on_delete=models.CASCADE,
                                           verbose_name='计划', related_name="api")
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.ForeignKey(GlobalHost, on_delete=models.DO_NOTHING, verbose_name='所属host')
    dubboMethod = models.CharField(max_length=1024, blank=True, null=True, verbose_name='DUBBO方法')
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='参数请求格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    formatRaw = models.BooleanField(default=False, verbose_name="是否转换成源数据")
    examineType = models.CharField(default='no_check', max_length=50, verbose_name='校验方式', choices=EXAMINE_TYPE_CHOICE)
    httpCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='返回内容')
    index = models.IntegerField(blank=True, null=True, verbose_name='排序')


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划接口'
        verbose_name_plural = '计划接口管理'


class AutomationHead(models.Model):
    """
    请求头
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.ForeignKey(AutomationScheduleApi, related_name='header',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容')
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


class AutomationParameter(models.Model):
    """
    请求的参数
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.ForeignKey(AutomationScheduleApi, related_name='parameterList',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '接口参数'
        verbose_name_plural = '接口参数管理'


class AutomationParameterRaw(models.Model):
    """
    请求的源数据参数
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.OneToOneField(AutomationScheduleApi, related_name='parameterRaw',
                                             on_delete=models.CASCADE, verbose_name='接口')
    data = models.TextField(verbose_name='源数据请求参数', blank=True, null=True)

    class Meta:
        verbose_name = '源数据参数'
        verbose_name_plural = '源数据参数管理'


class AutomationResponseJson(models.Model):
    """
    返回JSON参数
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.ForeignKey(AutomationScheduleApi, related_name='response',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='JSON参数', blank=True, null=True)
    tier = models.CharField(max_length=1024, verbose_name='层级关系', blank=True, null=True)
    type = models.CharField(max_length=1024, verbose_name="关联类型", default="json", choices=(('json', 'json'),('Regular', 'Regular')))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '结果JSON参数'
        verbose_name_plural = '结果JSON参数管理'


class AutomationTestResult(models.Model):
    """
    手动执行结果
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.OneToOneField(AutomationScheduleApi, on_delete=models.CASCADE, verbose_name='接口'
                                             , related_name="test_result")
    url = models.CharField(max_length=1024, verbose_name='请求地址')
    requestType = models.CharField(max_length=1024, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.CharField(max_length=1024, verbose_name='测试地址', null=True, blank=True)
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态', choices=HTTP_CODE_CHOICE)
    examineType = models.CharField(max_length=1024, verbose_name='匹配规则')
    data = models.TextField(blank=True, null=True, verbose_name='规则内容')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.DateTimeField(auto_now_add=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '手动测试结果'
        verbose_name_plural = '手动测试结果管理'


class AutomationTestTask(models.Model):
    """
    计划定时任务
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, verbose_name='项目')
    # host = models.ForeignKey(GlobalHost, on_delete=models.DO_NOTHING, verbose_name='HOST')
    Schedule = models.ForeignKey(AutomationTestSchedule, on_delete=models.CASCADE, verbose_name='计划ID')
    name = models.CharField(max_length=50, verbose_name='任务名称')
    type = models.CharField(max_length=50, verbose_name='类型', choices=TASK_CHOICE)
    frequency = models.IntegerField(blank=True, null=True, verbose_name='间隔')
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name='单位', choices=UNIT_CHOICE)
    startTime = models.DateTimeField(max_length=50, verbose_name='开始时间')
    endTime = models.DateTimeField(max_length=50, verbose_name='结束时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '计划定时任务'
        verbose_name_plural = '计划定时任务管理'


class AutomationTaskRunTime(models.Model):
    """
    计划执行开始和结束时间
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    startTime = models.CharField(max_length=50, verbose_name='开始时间')
    host = models.CharField(max_length=1024, null=True, blank=True, verbose_name='测试地址')
    elapsedTime = models.CharField(max_length=50, verbose_name='结束时间')
    Schedule = models.ForeignKey(AutomationTestSchedule, on_delete=models.CASCADE, verbose_name='计划ID')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)


    class Meta:
        verbose_name = '计划任务执行时间'
        verbose_name_plural = '计划任务执行时间'


class AutomationScheduleTestResult(models.Model):
    """
    任务执行结果
    """
    id = models.AutoField(primary_key=True)
    automationScheduleApi = models.ForeignKey(AutomationScheduleApi, on_delete=models.CASCADE, verbose_name='接口'
                                          , related_name="auto_result")
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseHeader = models.TextField(blank=True, null=True, verbose_name='返回头')
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.CharField(max_length=128, null=True, blank=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '自动测试结果'
        verbose_name_plural = '自动测试结果管理'


class AutomationReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")

    def __unicode__(self):
        return self.reportFrom

    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"


class VisitorsRecord(models.Model):
    """
    访客记录
    """
    id = models.AutoField(primary_key=True)
    formattedAddress = models.CharField(max_length=1024, blank=True, null=True, verbose_name="访客地址")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="国家")
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name="省份")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="城市")
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name="县级")
    township = models.CharField(max_length=50, blank=True, null=True, verbose_name="镇")
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name="街道")
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name="门牌号")
    success = models.CharField(max_length=50, blank=True, null=True, verbose_name="成功")
    reason = models.CharField(max_length=1024, blank=True, null=True, verbose_name="原因")
    callTime = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __unicode__(self):
        return self.formattedAddress

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = "访客查看"


class CaseProject(models.Model):
    """
    用例项目表
    """
    CaseProjectType = (
        ('手动', '手动'),
        ('自动化', '自动化')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='项目名称')
    version = models.CharField(max_length=50, verbose_name='版本')
    type = models.CharField(max_length=50, verbose_name='类型', choices=CaseProjectType)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')
    yn = models.BooleanField(default=False, verbose_name='逻辑删除')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例项目'
        verbose_name_plural = '用例项目'


class CaseProjectDynamic(models.Model):
    """
    用例项目动态
    """
    id = models.AutoField(primary_key=True)
    caseProject = models.ForeignKey(CaseProject, related_name='dynamic_case_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(max_length=128, verbose_name='操作时间')
    type = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, related_name='case_userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True,  verbose_name='描述')

    def __unicode__(self):
        return self.type

    def __str__(self):
        return str(self.time)

    class Meta:
        verbose_name = '用例项目动态'
        verbose_name_plural = '用例项目动态'


class CaseProjectMember(models.Model):
    """
    项目成员
    """
    CHOICES = (
        ('超级管理员', '超级管理员'),
        ('开发人员', '开发人员'),
        ('测试人员', '测试人员')
    )
    id = models.AutoField(primary_key=True)
    permissionType = models.CharField(max_length=50, verbose_name='权限角色', choices=CHOICES)
    caseProject = models.ForeignKey(CaseProject, related_name='member_case_project', on_delete=models.CASCADE,
                                    verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_case_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.permissionType

    def __str__(self):
        return self.permissionType

    class Meta:
        verbose_name = '用例项目成员'
        verbose_name_plural = '用例项目成员'


class CaseRequirement(models.Model):
    """
    用例需求
    """
    id = models.AutoField(primary_key=True)
    caseProject = models.ForeignKey(CaseProject, on_delete=models.CASCADE, verbose_name='项目',
                                    related_name='project_requirement')
    name = models.CharField(max_length=1024, blank=True, null=True, verbose_name='需求名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')
    zentao_id = models.CharField(max_length=50, null=True, default='0', verbose_name='蝉道ID')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    yn = models.BooleanField(default=False, verbose_name='逻辑删除')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例需求'
        verbose_name_plural = '用例需求'


class CaseInfo(models.Model):
    """
    用例信息
    """
    PriorityType = (
        ('p1', 'p1'),
        ('p2', 'p2'),
        ('p3', 'p3'),
        ('p4', 'p4')
    )

    ActualResult = (
        ('0', '未执行'),
        ('1', '通过'),
        ('2', '失败')
    )

    id = models.AutoField(primary_key=True)
    caseProject = models.ForeignKey(CaseProject, related_name='case_project', blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='所属项目')
    caseRequirement = models.ForeignKey(CaseRequirement, blank=True, null=True, related_name='case_requirement',
                                        on_delete=models.SET_NULL, verbose_name='所属需求')
    name = models.CharField(max_length=1024, verbose_name='用例名称')
    priority = models.CharField(max_length=50, default='p2', verbose_name='优先级', choices=PriorityType)
    testType = models.CharField(max_length=50, blank=True, null=True,verbose_name='测试类型')
    testTontent = models.CharField(max_length=1024, blank=True, null=True,verbose_name='测试内容')
    stage = MultiSelectField(verbose_name='测试阶段', default='1', choices=Stage)
    operationSteps = models.TextField(verbose_name='操作步骤')
    expectedResults = models.TextField(verbose_name='预期结果')
    actualResult = models.CharField(max_length=50, default='0', verbose_name='测试结果', choices=ActualResult)
    reason = models.CharField(max_length=1024, blank=True, null=True, verbose_name='原因')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    version = models.CharField(max_length=1024, blank=True, null=True, verbose_name='版本')
    hardware = models.CharField(max_length=1024, blank=True, null=True, verbose_name='硬件')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='更新人', related_name='CaseUpdateUser')
    yn = models.BooleanField(default=False, verbose_name='逻辑删除')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例信息'
        verbose_name_plural = '用例信息'


class CaseOperationHistory(models.Model):
    """
    用例操作历史
    """
    id = models.AutoField(primary_key=True)
    case = models.ForeignKey(CaseInfo, on_delete=models.CASCADE, verbose_name='用例')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='用户姓名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='操作内容')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = '用例操作历史'
        verbose_name_plural = '用例操作历史'


class CaseReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    caseProject = models.OneToOneField(CaseProject, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")

    def __unicode__(self):
        return self.reportFrom

    def __str__(self):
        return self.reportFrom
    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"

class ScriptGroup(models.Model):
    """
        脚本分组
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='脚本分组')
    status = models.CharField(max_length=1024, verbose_name='状态', default='1', choices=STATUS_CHOICE)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '脚本分组'
        verbose_name_plural = '脚本分组'

class Script(models.Model):
    """
    脚本信息表
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45,verbose_name="脚本名称")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    scriptGroup = models.ForeignKey(ScriptGroup, on_delete=models.SET_NULL, null=True,related_name='script_group',default='1', max_length=1024, verbose_name='所属脚本')
    status = models.CharField(max_length=1024,verbose_name='状态',default='1', choices=STATUS_CHOICE)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='更新人')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "脚本信息"
        verbose_name_plural = "脚本信息"



class ScriptFile(models.Model):
    """
    脚本详情：脚本文件，脚本名称，脚本内容
    """
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Script, on_delete=models.CASCADE,related_name='script_file', max_length=1024, verbose_name='所属脚本')
    fileName = models.CharField(max_length=45,verbose_name="脚本文件名称")
    fileDetail = models.TextField(verbose_name="脚本文件内容")
    status = models.CharField(max_length=1024,default='1',verbose_name='状态', choices=STATUS_CHOICE)
    executable = models.CharField(max_length=1024,default='1', verbose_name='是否可执行') #脚本的入口文件，默认值为1，可执行，一个脚本有且只能有一个入口文件
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='更新人')

    def __str__(self):
        return self.fileName

    class Meta:
        verbose_name = "脚本文件"
        verbose_name_plural = "脚本文件"


class ScriptRunResult(models.Model):
    """
    #执行结果信息
    """
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="script_result", max_length=1024,
                            verbose_name='所属脚本')
    result = models.TextField(verbose_name="脚本运行结果")
    logFilePath = models.CharField(max_length=1024,null=True,verbose_name="脚本日志路径")
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='更新人')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "脚本执行结果"
        verbose_name_plural = "脚本执行结果"


class ScriptOperationHistory(models.Model):
    """
    脚本操作历史
    """
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="script_history", max_length=1024,
                            verbose_name='所属脚本')
    modifyData = models.TextField(verbose_name="更改内容")
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='更新人')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "脚本操作历史"
        verbose_name_plural = "脚本操作历史"

class ScriptParameter(models.Model):
    """
    脚本依赖参数
    """
    id = models.AutoField(primary_key=True)
    sid = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="script_parameter", max_length=1024,
                            verbose_name='所属脚本')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    description = models.CharField(max_length=1024, null=True,verbose_name='参数描述')

    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    status = models.CharField(max_length=1024,default='1',verbose_name='状态', choices=STATUS_CHOICE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '脚本参数'
        verbose_name_plural = '脚本参数'
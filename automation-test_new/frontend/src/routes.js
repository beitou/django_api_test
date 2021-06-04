const NotFound = () => import('./views/common/404.vue');
const Login = () => import('./views/common/Login.vue');
const Home = () => import('./views/Home.vue');
const About = () => import('./views/About.vue');
const Script = () => import('./views/script/Script.vue');
const projectList = () => import('./views/Projectlist.vue');
const ProjectInfo = () => import('./views/Project.vue');
const ScriptEdit = () => import('./views/script/ScriptEdit.vue');
const ScriptInfo = () => import('./views/script/ScriptTitle.vue');
const QualityReport = () => import('./views/QualityReport.vue');
const LineBug = () => import('./views/LineBug.vue');
const globalHost = () => import('./views/project/global/Globalhost.vue');
const postman = () => import('./views/project/api/Postman.vue');
const API = () => import('./views/project/api/API.vue');
const ApiList = () => import('./views/project/api/ApiList.vue');
const ApiListGroup = () => import('./views/project/api/ApiListGroup.vue');
const FestTest = () => import('./views/project/api/FestTest.vue');
const addApi = () => import('./views/project/api/Addapi.vue');
const detail = () => import('./views/project/api/updateApi/ApiForm.vue');
const ApiInfo = () => import('./views/project/api/updateApi/ApiInfo.vue');
const testApi = () => import('./views/project/api/updateApi/TestApi.vue');
const UpdateApi = () => import('./views/project/api/updateApi/UpdateApi.vue');
const ApiDynamic = () => import('./views/project/api/updateApi/ApiDynamic.vue');
const AutomationTest = () => import('./views/project/automation/AutomationTest.vue');
const ScheduleList = () => import('./views/project/automation/ScheduleList.vue');
const ScheduleListGroup = () => import('./views/project/automation/ScheduleListGroup.vue');
const ScheduleApiList = () => import('./views/project/automation/ScheduleApiList.vue');
const AddScheduleApi = () => import('./views/project/automation/AddScheduleApi.vue');
const UpdateScheduleApi = () => import('./views/project/automation/UpdateScheduleApi.vue');
const TestReport = () => import('./views/project/automation/TestReport.vue');
const ProjectMember = () => import('./views/project/ProjectMember.vue');
const ProjectDynamic = () => import('./views/project/ProjectDynamic.vue');
const ProjectTitle = () => import('./views/project/projectTitle/ProjectTitle.vue');
const ProjectReport = () => import('./views/project/ProjectReport.vue');
const CaseProjectList = () => import('./views/CaseProjectList.vue');
const CaseProjectInfo = () => import('./views/CaseProject.vue');
const CaseProjectTitle = () => import('./views/caseProject/CaseProjectTitle.vue');
const CaseRequirement = () => import('./views/caseProject/CaseRequirement.vue');
const Case = () => import('./views/caseProject/Case.vue');
const CaseList = () => import('./views/caseProject/case/CaseList.vue');
const AddCase = () => import('./views/caseProject/case/AddCase.vue');
const CaseDetail = () => import('./views/caseProject/case/CaseDetail.vue');
const CaseInfo = () => import('./views/caseProject/case/caseDetail/CaseInfo.vue');
const CaseDynamic = () => import('./views/caseProject/case/caseDetail/CaseDynamic.vue');
const UpdateCase = () => import('./views/caseProject/case/UpdateCase.vue');
const CaseProjectMember = () => import('./views/caseProject/CaseProjectMember.vue');
const CaseProjectDynamic = () => import('./views/caseProject/CaseProjectDynamic.vue');
const CaseRequirementDetail = () => import('./views/caseProject/caseRequirement/CaseRequirementDetail.vue');
const CaseRequirementList = () => import('./views/caseProject/caseRequirement/CaseRequirementList.vue');
const CaseRequirementInfo = () => import('./views/caseProject/caseRequirement/caseRequirementDetail/CaseRequirementInfo.vue');
const CaseRequirementBug = () => import('./views/caseProject/caseRequirement/caseRequirementDetail/CaseRequirementBug.vue');
const CaseRequirementMail = () => import('./views/caseProject/caseRequirement/caseRequirementDetail/CaseRequirementMail.vue');



let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true,
        projectHidden: true,

    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true,
        projectHidden: true,

    },
    {
        path: '/',
        component: Home,
        name: '',
        projectHidden: true,

        children: [
            { path: '/projectList', component: projectList, iconCls:'el-icon-menu', name: '项目列表'},
            { path: '/caseProjectList', component: CaseProjectList, iconCls:'el-icon-menu', name: '需求项目'},
            // { path: '/robot', component: robot, iconCls:'fa fa-id-card-o', name: '消息机器人', meta: { keepAlive: false }},
            { path: '/Script', component: Script, iconCls:'el-icon-tickets', name: '脚本列表'},
            { path: '/qualityReport', component: QualityReport, iconCls:'el-icon-tickets', name: '质量报告'},
            { path: '/lineBug', component: LineBug, iconCls:'el-icon-tickets', name: '质量数据'},
            // { path: '/teamBug', component: TeamBug, iconCls:'el-icon-tickets', name: 'bug数统计'},
            { path: '/about', component: About, iconCls:'el-icon-share', name: '关于'},
        ]
    },
    {
        path: '*',
        hidden: true,
        projectHidden: true,

        redirect: { path: '/404' }
    },
    {
        path: '/Script/script=:script_id',
        component: ScriptEdit,
        name: '编辑脚本',
        hidden: true,
        isapiproject:false,
        children:[
            {   path: '/ScriptInfo/scrpit=:script_id', component: ScriptInfo, name: '脚本查看', leaf: true},
        ]

    },
    {
        path: '/project/project=:project_id',
        component: ProjectInfo,
        name: '项目',
        hidden: true,
        isapiproject:true,
        children: [
            {   path: '/ProjectTitle/project=:project_id', component: ProjectTitle, name: '项目概况', leaf: true},
            {   path: '/GlobalHost/project=:project_id', component: globalHost, name: 'Host配置', leaf: true},
            {   path: '/api/project=:project_id',
                    component: API,
                    name: 'API接口',
                    leaf: true,
                    child: true,
                    children: [
                        {   path: '/apiList/project=:project_id', component: ApiList, name: '接口列表'},
                        {   path: '/apiList/project=:project_id/first=:firstGroup', component: ApiListGroup, name: '分组接口列表'},
                        {   path: '/fastTest/project=:project_id', component: FestTest, name: '快速测试'},
                        {   path: '/addApi/project=:project_id', component: addApi, name: '新增接口'},
                        {   path: '/caseDetail/project=:project_id/api=:api_id',
                            component: detail,
                            name: '接口',
                            children: [
                                { path: '/apiInfo/project=:project_id/api=:api_id', component: ApiInfo, name: '基础信息'},
                                { path: '/testApi/project=:project_id/api=:api_id', component: testApi, name: '测试'},
                                { path: '/apiDynamic/project=:project_id/api=:api_id', component: ApiDynamic, name: '历史'},
                            ]
                        },
                        { path: '/updateApi/project=:project_id/api=:api_id', component: UpdateApi, name: '修改'},
                    ]},
            {   path: '/automationTest/project=:project_id',
                    component: AutomationTest,
                    name: '自动化测试',
                    leaf: true,
                    child: true,
                    children: [
                        {   path: '/scheduleList/project=:project_id', component: ScheduleList, name: '计划列表'},
                        {   path: '/scheduleList/project=:project_id/first=:firstGroup', component: ScheduleListGroup, name: '分组计划列表'},
                        {   path: '/scheduleApiList/project=:project_id/schedule=:schedule_id', component: ScheduleApiList, name: '计划接口列表'},
                        {   path: '/addScheduleApi/project=:project_id/schedule=:schedule_id', component: AddScheduleApi, name: '添加新接口'},
                        {   path: '/updateScheduleApi/project=:project_id/schedule=:schedule_id/api=:api_id', component: UpdateScheduleApi, name: '修改接口'},
                        {   path: '/testReport/project=:project_id/schedule=:schedule_id', component: TestReport, name: '测试报告'},
                    ]
            },
            {   path: '/projectMember/project=:project_id', component: ProjectMember, name: '成员管理', leaf: true},
            {   path: '/projectDynamic/project=:project_id', component: ProjectDynamic, name: '项目动态', leaf: true},
            {   path: '/projectReport/project=:project_id', component: ProjectReport, name: '自动化测试报告', leaf: true},
            ]
    },
    {
        path: '/caseProject/caseProject=:caseProject_id',
        component: CaseProjectInfo,
        name: '需求项目',
        hidden: true,
        isCaseProject:true,
        children: [
            {   path: '/caseProjectTitle/caseProject=:caseProject_id', component: CaseProjectTitle, name: '需求项目概况', leaf: true},
            {   path: '/caseRequirement/caseProject=:caseProject_id',
                    component: CaseRequirement,
                    name: '需求',
                    leaf: true,
                    child: true,
                    children: [
                        {   path: '/caseRequirementList/caseProject=:caseProject_id', component: CaseRequirementList, name: '用例需求列表'},
                        {   path: '/caseRequirementDetail/caseProject=:caseProject_id/caseRequirement_id=:caseRequirement_id',
                            component: CaseRequirementDetail,
                            name: '需求概况',
                            children: [
                                { path: '/caseRequirementInfo/caseProject=:caseProject_id/caseRequirement_id=:caseRequirement_id', component: CaseRequirementInfo, name: '需求基础信息'},
                                { path: '/caseRequirementBug/caseProject=:caseProject_id/caseRequirement_id=:caseRequirement_id/zenTao=:zenTao_id', component: CaseRequirementBug, name: 'Bug详情'},
                                { path: '/caseRequirementMail/caseProject=:caseProject_id/caseRequirement_id=:caseRequirement_id', component: CaseRequirementMail, name: '邮件发送'},
                            ]
                        },
                    ]
            },
            {   path: '/case/caseProject=:caseProject_id',
                    component: Case,
                    name: '用例',
                    leaf: true,
                    child: true,
                    children: [
                        {   path: '/caseList/caseProject=:caseProject_id', component: CaseList, name: '用例列表'},
                        {   path: '/caseList/caseProject=:caseProject_id/caseRequirement=:caseRequirement_id', component: CaseList, name: '需求用例列表'},
                        {   path: '/addCase/caseProject=:caseProject_id', component: AddCase, name: '新增用例'},
                        {   path: '/caseDetail/caseProject=:caseProject_id/case=:case_id',
                            component: CaseDetail,
                            name: '用例信息',
                            children: [
                                { path: '/caseInfo/caseProject=:caseProject_id/case=:case_id', component: CaseInfo, name: '用例基础信息'},
                                { path: '/caseInfo/caseProject=:caseProject_id/case=:case_id', component: CaseInfo, name: '用例需求基础信息'},
                                { path: '/caseDynamic/caseProject=:caseProject_id/case=:case_id', component: CaseDynamic, name: '用例历史'},
                            ]
                        },
                        { path: '/updateCase/caseProject=:caseProject_id/case=:case_id', component: UpdateCase, name: '修改用例'},
                    ]},
            {   path: '/caseProjectMember/caseProject=:caseProject_id', component: CaseProjectMember, name: '用例成员管理', leaf: true},
            {   path: '/caseProjectDynamic/caseProject=:caseProject_id', component: CaseProjectDynamic, name: '用例项目动态', leaf: true},
            ]
    },
];

export default routes;
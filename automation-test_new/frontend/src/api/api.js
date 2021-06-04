import axios from 'axios';

//export const test = 'http://127.0.0.1:8000';
//export const test = 'http://172.16.116.60:8000';
export const   test = process.env.BASE_API;
// 登录
export const requestLogin = params => { return axios.post(`${test}/api/user/login`, params).then(res => res.data); };
// 记录访客
export const recordVisitor = params => { return axios.post(`${test}/api/user/VisitorRecord`, params).then(res => res.data); };
// 获取项目
export const getProject = (headers, params) => {
    return axios.get(`${test}/api/project/project_list`, { params: params, headers:headers}).then(res => res.data); };
// 删除项目
export const delProject = (headers, params) => {
    return axios.post(`${test}/api/project/del_project`, params, {headers}).then(res => res.data); };

export const uploadFile = (headers, params) => {
    return axios.post(`${test}/api/script/upload_file`, params, {headers}).then(res => res.data); };

export const getFileDetail = (headers, params) => {
    return axios.get(`${test}/api/script/getFileDetail`, { params: params, headers:headers}).then(res => res.data); };

export const delFile = (headers, params) => {
    return axios.post(`${test}/api/script/deleteFile`, params, {headers}).then(res => res.data); };

export const updateFile = (headers, params) => {
    return axios.post(`${test}/api/script/updateFile`, params, {headers}).then(res => res.data); };

//添加脚本
export const addScript = (headers, params) => {
    return axios.post(`${test}/api/script/addScript`, params, {headers}).then(res => res.data); };

export const getScriptList = (headers, params) => {
    return axios.get(`${test}/api/script/scriptList`, { params: params, headers:headers}).then(res => res.data); };

export const scriptGroupList = (headers, params) => {
    return axios.get(`${test}/api/script/scriptGroupList`, { params: params, headers:headers}).then(res => res.data); };

export const addScriptGroup = (headers, params) => {
    return axios.post(`${test}/api/script/addScriptGroup`, params, {headers}).then(res => res.data); };

export const delScriptGroup = (headers, params) => {
    return axios.post(`${test}/api/script/delScriptGroup`, params, {headers}).then(res => res.data); };



export const delScript = (headers, params) => {
    return axios.post(`${test}/api/script/delScript`, params, {headers}).then(res => res.data); };

export const getScript = (headers, params) => {
    return axios.get(`${test}/api/script/getScript`, { params: params, headers:headers}).then(res => res.data); };

export const UpdateScript = (headers, params) => {
    return axios.post(`${test}/api/script/updateScript`, params, {headers}).then(res => res.data); };

export const runScript = (headers, params) => {
    return axios.post(`${test}/api/script/runScript`, params, {headers}).then(res => res.data); };



// 禁用项目
export const disableProject = (headers, params) => {
    return axios.post(`${test}/api/project/disable_project`, params, {headers}).then(res => res.data); };
// 启用项目
export const enableProject = (headers, params) => {
    return axios.post(`${test}/api/project/enable_project`, params, {headers}).then(res => res.data); };
// 修改项目
export const updateProject = (headers, params) => {
    return axios.post(`${test}/api/project/update_project`, params, {headers}).then(res => res.data); };
// 添加项目
export const addProject = (headers, params) => {
    return axios.post(`${test}/api/project/add_project`, params, {headers}).then(res => res.data); };
// 获取项目详情
export const getProjectDetail = (headers, params) => {
    return axios.get(`${test}/api/title/project_info`, { params: params, headers:headers}).then(res => res.data); };
// 获取测试地址列表
export const getHost = (headers, params) => {
    return axios.get(`${test}/api/global/host_total`, { params: params, headers:headers}).then(res => res.data); };
// 删除测试地址列表
export const delHost = (headers, params) => {
    return axios.post(`${test}/api/global/del_host`, params, {headers}).then(res => res.data); };
// 禁用测试地址列表
export const disableHost = (headers, params) => {
    return axios.post(`${test}/api/global/disable_host`, params, {headers}).then(res => res.data); };
// 启用测试地址列表
export const enableHost = (headers, params) => {
    return axios.post(`${test}/api/global/enable_host`, params, {headers}).then(res => res.data); };
// 修改测试地址列表
export const updateHost = (headers, params) => {
    return axios.post(`${test}/api/global/update_host`, params, {headers}).then(res => res.data); };
// 添加测试地址列表
export const addHost = (headers, params) => {
    return axios.post(`${test}/api/global/add_host`, params, {headers}).then(res => res.data); };
// 获取项目动态
export const getProjectDynamicList = (headers, params) => {
    return axios.get(`${test}/api/dynamic/dynamic`, { params: params, headers:headers}).then(res => res.data); };
// 获取项目成员
export const getProjectMemberList = (headers, params) => {
    return axios.get(`${test}/api/member/project_member`, { params: params, headers:headers}).then(res => res.data); };
// 获取发送邮件配置
export const getEmailConfigDetail = (headers, params) => {
    return axios.get(`${test}/api/member/get_email`, { params: params, headers:headers}).then(res => res.data); };
// 删除邮件配置
export const delEmailConfig = (headers, params) => {
    return axios.post(`${test}/api/member/del_email`, params, {headers}).then(res => res.data); };
// 添加邮件配置
export const addEmailConfig = (headers, params) => {
    return axios.post(`${test}/api/member/email_config`, params, {headers}).then(res => res.data); };
// 获取自动化测试结果
export const getTestResultList = (headers, params) => {
    return axios.get(`${test}/api/report/auto_test_report`, { params: params, headers:headers}).then(res => res.data); };
// 获取最近10次测试时间
export const getTestTenTime = (headers, params) => {
    return axios.get(`${test}/api/report/test_time`, { params: params, headers:headers}).then(res => res.data); };
// 获取最近10次测试比例结果
export const getTestTenResult = (headers, params) => {
    return axios.get(`${test}/api/report/lately_ten`, { params: params, headers:headers}).then(res => res.data); };

// 添加接口
export const addApiDetail = (headers, params) => {
    return axios.post(`${test}/api/api/add_api`, params, {headers}).then(res => res.data); };
// 获取接口分组列表
export const getApiGroupList = (headers, params) => {
    return axios.get(`${test}/api/api/group`, { params: params, headers:headers}).then(res => res.data); };
// 添加接口分组
export const addApiGroup = (headers, params) => { return axios.post(`${test}/api/api/add_group`, params, {headers}).then(res => res.data); };
// 修改接口分组
export const updateApiGroup = (headers, params) => {
    return axios.post(`${test}/api/api/update_name_group`, params, {headers}).then(res => res.data); };
// 删除接口分组
export const delApiGroup = (headers, params) => {
    return axios.post(`${test}/api/api/del_group`, params, {headers}).then(res => res.data); };
// 获取用例项目
export const getCaseProject = (headers, params) => {
    return axios.get(`${test}/api/caseProject/caseProject_list`, { params: params, headers:headers}).then(res => res.data); };
// 删除用例项目
export const delCaseProject = (headers, params) => {
    return axios.post(`${test}/api/caseProject/del_CaseProject`, params, {headers}).then(res => res.data); };
// 添加用例项目
export const addCaseProject = (headers, params) => {
    return axios.post(`${test}/api/caseProject/add_CaseProject`, params, {headers}).then(res => res.data); };
// 修改用例项目
export const updateCaseProject = (headers, params) => {
    return axios.post(`${test}/api/caseProject/update_CaseProject`, params, {headers}).then(res => res.data); };
// 禁用用例项目
export const disableCaseProject = (headers, params) => {
    return axios.post(`${test}/api/caseProject/disable_CaseProject`, params, {headers}).then(res => res.data); };
// 禁用用例项目
export const enableCaseProject = (headers, params) => {
    return axios.post(`${test}/api/caseProject/enable_CaseProject`, params, {headers}).then(res => res.data); };
// 获取用例项目详情
export const getCaseProjectDetail = (headers, params) => {
    return axios.get(`${test}/api/title/caseProject_info`, { params: params, headers:headers}).then(res => res.data); };
// 获取需求列表
export const getCaseRequirement = (headers, params) => {
    return axios.get(`${test}/api/caseRequirement/requirement_total`, { params: params, headers:headers}).then(res => res.data); };
// 添加需求
export const addCaseRequirement = (headers, params) => {
    return axios.post(`${test}/api/caseRequirement/add_CaseRequirement`, params, {headers}).then(res => res.data); };
// 删除需求
export const delCaseRequirement = (headers, params) => {
    return axios.post(`${test}/api/caseRequirement/del_CaseRequirement`, params, {headers}).then(res => res.data); };
// 编辑需求
export const updateCaseRequirement = (headers, params) => {
    return axios.post(`${test}/api/caseRequirement/update_CaseRequirement`, params, {headers}).then(res => res.data); };
export const getCaseProjectMemberList = (headers, params) => {
    return axios.get(`${test}/api/member/caseProjectMember`,{ params: params, headers:headers}).then(res=>res.data);
};
export const addCaseProjectEmail = (headers, params) => {
    return axios.post(`${test}/api/member/caseEmailConfig`,params,{headers}).then(res=>res.data);
};
export const delCaseProjectEmail = (headers, params) => {
    return axios.post(`${test}/api/member/caseDelEmail`,params,{headers}).then(res=>res.data);
};
export const getCaseProjectEmail = (headers, params) => {
    return axios.get(`${test}/api/member/caseGetEmail`,{ params: params, headers:headers}).then(res=>res.data);
};

export const requrl = (headers, params) => {
    return axios.get(`${test}/api/request/url`,{ params: params, headers:headers}).then(res=>res.data);
};
export const requrl_post = (headers, params) => {
    return axios.post(`${test}/api/request/url`,params, {headers}).then(res=>res.data);
};
// 获取用例列表
export const getCase = (headers, params) => {
    return axios.get(`${test}/api/case/case_total`, { params: params, headers:headers}).then(res => res.data); };
// 获取用例信息
export const getCaseInfo = (headers, params) => {
    return axios.get(`${test}/api/case/case_info`, { params: params, headers:headers}).then(res => res.data); };
// 添加用例
export const addCase = (headers, params) => {
    return axios.post(`${test}/api/case/add_Case`, params, {headers}).then(res => res.data); };
// 更新用例
export const updateCase = (headers, params) => {
    return axios.post(`${test}/api/case/update_Case`, params, {headers}).then(res => res.data); };
// 删除用例
export const delCase = (headers, params) => {
    return axios.post(`${test}/api/case/del_Case`, params, {headers}).then(res => res.data); };
// 获取用例操作记录
export const getCaseDynamic = (headers, params) => {
    return axios.get(`${test}/api/case/case_dynamic`, { params: params, headers:headers}).then(res => res.data); };
// 获取用例项目动态
export const getCaseProjectDynamicList = (headers, params) => {
    return axios.get(`${test}/api/caseProjectDynamic/dynamic`, { params: params, headers:headers}).then(res => res.data); };
//从Excel导入测试用例
export const importCase = (headers, params) => {
    return axios.post(`${test}/api/case/import_case`, params, {headers}).then(res => res.data); };
//从Excel导出测试用例
export const ExportCaseExcel = (headers, params) => {
    return axios.get(`${test}/api/case/export_case`, { params: params, headers:headers}).then(res => res.data); };
//下载文档
export const DownloadDoc = (headers, params) => {
    return axios.get(`${test}/api/case/export_case`, { params: params, headers:headers}).then(res => res.data); };
//脚本执行
export const runCode = (headers, params) => {
    return axios.post(`${test}/api/case/run_code`, params, {headers}).then(res => res.data); };
//获取蝉道bug
export const getZentaoBug = (headers, params) => {
    return axios.get(`${test}/api/case/zentao_bug`, { params: params, headers:headers}).then(res => res.data); };
//统计git代码行数
export const getGitAllLine = (headers, params) => {
    return axios.get(`${test}/api/qualityReport/getGitAllLine`, { params: params, headers:headers}).then(res => res.data); };
//统计千行代码bug率
export  const getCodeQuality = (headers, params)=> {
    return axios.get(`${test}/api/lineBug/getCodeQuality`, {params: params, headers:headers}).then(res => res.data); };
//获取分组bug数
export const getTeamBug = (headers, params) => {
    return axios.get(`${test}/api/count/team_bug_count`, { params: params, headers:headers}).then(res => res.data); };



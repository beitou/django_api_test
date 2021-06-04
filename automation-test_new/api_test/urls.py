from django.conf.urls import url

from api_test.api import ApiDoc, automationSchedule as Schedule, member, dynamic, user, VisitorRecord
from api_test.api import automationReport as Report
from api_test.api.global_parameter import HostTotal, AddHost, UpdateHost, DelHost, DisableHost, EnableHost
from api_test.api.projectList import ProjectList, AddProject, DelProject, \
    EnableProject, UpdateProject, DisableProject
from api_test.api.projectTitle import ProjectInfo
from api_test.case.case import CaseList, AddCase, CaseInformation, UpdateCase, DelCase, CaseDynamic, CaseExportExcel
from api_test.case.caseProjectExport import ExportCaseExcel
from api_test.case.caseProjectList import CaseProjectList, AddCaseProject, DelCaseProject, UpdateCaseProject, \
    DisableCaseProject, EnableCaseProject
from api_test.case.caseProjectTitle import CaseProjectInfo
from api_test.case.caseRequirementList import CaseRequirementList, AddCaseRequiremen, DelCaseRequiremen, \
    UpdateCaseRequiremen
from api_test.case import caseProjectMember, caseProjectDynamic
from api_test.case.requirementBug import RequirementBug
from api_test.common import http_request
from api_test.common.customUrl import CustomUrl
from api_test.qualityReport.code_quality import CodeQuality
from api_test.qualityReport.gitLabLine import GitLabLine
from api_test.script.runScript import RunScript
from api_test.script import uploadFile, script_group

from api_test.case.loadCaseFromExcel import ImportCaseFromExcel
from api_test.script.script import AddScript, ScriptList, DelScript, UpdateScript, GetScript, AddRunResult, \
    AddHistory, HistoryList
from api_test.script.runCode import RunCode

urlpatterns = [
    url(r'project/project_list', ProjectList.as_view()),
    url(r'script/upload_file', uploadFile.uploadFile.as_view()),
    url(r'script/getFileDetail', uploadFile.getFileDetail.as_view()),
    url(r'script/deleteFile', uploadFile.deleteFile.as_view()),
    url(r'script/updateFile', uploadFile.updateFile.as_view()),

    url(r'script/scriptGroupList', script_group.ScriptGroupList.as_view()),
    url(r'script/addScriptGroup', script_group.AddScriptGroup.as_view()),
    url(r'script/delScriptGroup', script_group.DelScriptGroup.as_view()),

    url(r'script/addScript', AddScript.as_view()),
    url(r'script/scriptList', ScriptList.as_view()),
    url(r'script/delScript', DelScript.as_view()),
    url(r'script/updateScript', UpdateScript.as_view()),
    url(r'script/getScript', GetScript.as_view()),
    url(r'script/runScript', RunScript.as_view()),
    url(r'script/addRunResult', AddRunResult.as_view()),
    url(r'script/addHistory', AddHistory.as_view()),
    url(r'script/historyList', HistoryList.as_view()),

    url(r'project/add_project', AddProject.as_view()),
    url(r'project/update_project', UpdateProject.as_view()),
    url(r'project/del_project', DelProject.as_view()),
    url(r'project/disable_project', DisableProject.as_view()),
    url(r'project/enable_project', EnableProject.as_view()),
    url(r'title/project_info', ProjectInfo.as_view()),
    url(r'global/host_total', HostTotal.as_view()),
    url(r'global/add_host', AddHost.as_view()),
    url(r'global/update_host', UpdateHost.as_view()),
    url(r'global/del_host', DelHost.as_view()),
    url(r'global/disable_host', DisableHost.as_view()),
    url(r'global/enable_host', EnableHost.as_view()),
    url(r'api/group', ApiDoc.Group.as_view()),
    url(r'api/add_group', ApiDoc.AddGroup.as_view()),
    url(r'api/update_name_group', ApiDoc.UpdateNameGroup.as_view()),
    url(r'api/del_group', ApiDoc.DelGroup.as_view()),
    url(r'api/api_list', ApiDoc.ApiList.as_view()),
    url(r'api/add_api', ApiDoc.AddApi.as_view()),
    url(r'api/updateMock', ApiDoc.UpdateApiMockStatus.as_view()),
    url(r'api/lead_swagger', ApiDoc.LeadSwagger.as_view()),
    url(r'api/update_api', ApiDoc.UpdateApi.as_view()),
    url(r'api/del_api', ApiDoc.DelApi.as_view()),
    url(r'api/update_group', ApiDoc.UpdateGroup.as_view()),
    url(r'api/api_info', ApiDoc.ApiInfoDetail.as_view()),
    url(r'api/add_history', ApiDoc.AddHistory.as_view()),
    url(r'api/history_list', ApiDoc.HistoryList.as_view()),
    url(r'api/del_history', ApiDoc.DelHistory.as_view()),
    url(r'api/operation_history', ApiDoc.OperationHistory.as_view()),
    url(r'api/Download', ApiDoc.DownLoad.as_view()),
    url(r'api/download_doc', ApiDoc.download_doc),
    url(r'automation/group', Schedule.Group.as_view()),
    url(r'automation/add_group', Schedule.AddGroup.as_view()),
    url(r'automation/del_group', Schedule.DelGroup.as_view()),
    url(r'automation/update_name_group', Schedule.UpdateNameGroup.as_view()),
    url(r'automation/update_schedule_group', Schedule.UpdateGroup.as_view()),
    url(r'automation/schedule_list', Schedule.ScheduleList.as_view()),
    url(r'automation/add_schedule', Schedule.AddSchedule.as_view()),
    url(r'automation/update_schedule', Schedule.UpdateSchedule.as_view()),
    url(r'automation/del_schedule', Schedule.DelSchedule.as_view()),
    url(r'automation/Downloadschedule', Schedule.DownLoadSchedule.as_view()),
    url(r'automation/api_list', Schedule.ApiList.as_view()),
    url(r'automation/update_api_list_index', Schedule.update_api_list_index.as_view()),
    url(r'automation/api_info', Schedule.ScheduleApiInfo.as_view()),
    url(r'automation/add_new_api', Schedule.AddNewApi.as_view()),
    url(r'automation/get_correlation_response', Schedule.GetCorrelationResponse.as_view()),
    url(r'automation/add_old_api', Schedule.AddOldApi.as_view()),
    url(r'automation/update_api', Schedule.UpdateApi.as_view()),
    url(r'automation/del_api', Schedule.DelApi.as_view()),
    url(r'automation/start_test', Schedule.StartTest.as_view()),
    url(r'automation/add_time_task', Schedule.AddTimeTask.as_view()),
    url(r'automation/get_time_task', Schedule.GetTask.as_view()),
    url(r'automation/del_task', Schedule.DelTask.as_view()),
    url(r'automation/look_result', Schedule.LookResult.as_view()),
    url(r'automation/test_report', Schedule.TestReport.as_view()),
    url(r'report/auto_test_report', Report.AutoTestReport.as_view()),
    # url(r'report/test_time', Report.TestTime.as_view()),
    # url(r'report/lately_ten', Report.AutoLatelyTenTime.as_view()),
    url(r'member/project_member', member.ProjectMemberList.as_view()),
    url(r'member/email_config', member.EmailConfig.as_view()),
    url(r'member/del_email', member.DelEmail.as_view()),
    url(r'member/get_email', member.GetEmail.as_view()),
    url(r'dynamic/dynamic', dynamic.Dynamic.as_view()),
    url(r'user/login', user.obtain_auth_token),
    url(r'user/VisitorRecord', VisitorRecord.Record.as_view()),
    url(r'caseProject/caseProject_list', CaseProjectList.as_view()),
    url(r'caseProject/add_CaseProject', AddCaseProject.as_view()),
    url(r'caseProject/del_CaseProject', DelCaseProject.as_view()),
    url(r'caseProject/update_CaseProject', UpdateCaseProject.as_view()),
    url(r'caseProject/disable_CaseProject', DisableCaseProject.as_view()),
    url(r'caseProject/enable_CaseProject', EnableCaseProject.as_view()),
    url(r'caseProject/exportCaseExcel', ExportCaseExcel.as_view()),
    url(r'title/caseProject_info', CaseProjectInfo.as_view()),
    url(r'caseRequirement/requirement_total', CaseRequirementList.as_view()),
    url(r'caseRequirement/add_CaseRequirement', AddCaseRequiremen.as_view()),
    url(r'caseRequirement/del_CaseRequirement', DelCaseRequiremen.as_view()),
    url(r'caseRequirement/update_CaseRequirement', UpdateCaseRequiremen.as_view()),
    url(r'case/case_total', CaseList.as_view()),
    url(r'case/case_info', CaseInformation.as_view()),
    url(r'member/caseProjectMember', caseProjectMember.ProjectMemberList.as_view()),
    url(r'member/caseEmailConfig', caseProjectMember.EmailConfig.as_view()),
    url(r'member/caseDelEmail', caseProjectMember.DelEmail.as_view()),
    url(r'member/caseGetEmail', caseProjectMember.GetEmail.as_view()),
    url(r'case/add_Case', AddCase.as_view()),
    url(r'case/update_Case', UpdateCase.as_view()),
    url(r'case/del_Case', DelCase.as_view()),
    url(r'caseProjectDynamic/dynamic', caseProjectDynamic.Dynamic.as_view()),
    url(r'case/case_dynamic', CaseDynamic.as_view()),
    url(r'case/import_case', ImportCaseFromExcel.as_view()),
    url(r'case/run_code', RunCode.as_view()),
    url(r'case/zentao_bug', RequirementBug.as_view()),
    url(r'request/url', http_request.httpRequest.as_view()),
    url(r'request/customUrl', CustomUrl.as_view()),
    url(r'qualityReport/getGitAllLine', GitLabLine.as_view()),
    url(r'lineBug/getCodeQuality', CodeQuality.as_view()),
    url(r'case/export_case', CaseExportExcel.as_view()),
    # url(r'count/team_bug_count', CodeQuality.as_view()),
]


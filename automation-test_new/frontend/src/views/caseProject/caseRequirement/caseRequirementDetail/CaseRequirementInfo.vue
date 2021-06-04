<template>
    <div class="main">
        <el-row :span="24">
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{ name: '需求用例列表', params: {caseProject_id: $route.params.caseProject_id, caseRequirement_id: $route.params.caseRequirement_id}}" style='text-decoration: none;color: #000000;'>
                        <h1>{{caseRequirementCount}}条用例</h1>
                    </router-link>
                    <div>需求用例数</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{casePassCount}}条通过</h1>
                    <div>通过用例数</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{caseFailCount}}条失败</h1>
                    <div>失败用例数</div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{passingRate}}</h1>
                    <div>通过率</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{smokePassingRate}}</h1>
                    <div>冒烟通过率</div>
                </el-card>
            </el-col>
        </el-row>
        <!--<el-row :span="24">-->
            <!--<el-col :span="6" class='inline'>-->
                <!--<el-card class="box-card">-->
                    <!--<router-link :to="{name: '用例成员管理'}" style='text-decoration: none;color: #000000;'><h1><img src="../../assets/member.png" class="member">{{memberCount}}人</h1></router-link>-->
                    <!--<div>项目组成员</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
            <!--&lt;!&ndash;暂时无用&ndash;&gt;-->
            <!--<el-col :span="6" class='inline'>-->
                <!--<el-card class="box-card">-->
                    <!--<router-link :to="{name: '计划列表'}" style='text-decoration: none;color: #000000;'><h1>自动化测试</h1></router-link>-->
                    <!--<div>自由测试接口并生成测试报告</div>-->
                <!--</el-card>-->
            <!--</el-col>-->
        <!--</el-row>-->
        <el-row :span="24">
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{createDate}}</h1>
                    <div>创建时间</div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import { getCaseProjectDetail, getCaseRequirement } from '../../../../api/api'
    export default {
        data() {
            return {
                type: '',
                version: '',
                updateDate: '',
                caseCount: 0,
                statusCount: 0,
                dynamicCount: 0,
                memberCount: 0,
                createDate: '',
                caseRequirementCount: '0',
                casePassCount: '0',
                caseFailCount: '0',
                passingRate: '0%',
                smokePassingRate: '0%',
            }
        },
        methods: {
            getRequirement() {
                this.listLoading = true;
                let self = this;
                let params = {
                    caseProject_id: this.$route.params.caseProject_id,
                    id: this.$route.params.caseRequirement_id,
                    page: self.page,
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getCaseRequirement(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.caseRequirementCount = data.data[0].caseRequirementCount;
                        self.casePassCount = data.data[0].casePassCount;
                        self.caseFailCount = data.data[0].caseFailCount;
                        self.passingRate = data.data[0].passingRate * 100 + '%';
                        self.createDate = data.data[0].createTime;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            getCaseProjectInfo() {
                var self = this;
                let params = { caseProject_id: this.$route.params.caseProject_id};
                let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                getCaseProjectDetail(headers, params).then(_data => {
                   let { msg, code, data } = _data;
                   self.listLoading = false;
                        if (code === '999999') {
                            self.type = data.type;
                            self.version = data.version;
                            self.updateDate = data.LastUpdateTime;
                            self.caseCount = data.caseCount;
                            self.dynamicCount = data.dynamicCount;
                            self.memberCount = data.memberCount;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                });
            }
        },
        mounted() {
            this.getCaseProjectInfo();
            this.getRequirement();
        }
    }
</script>

<style lang="scss" scoped>
    .box-card {
        width: 100%;
        height: 100%;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .member {
        width: 7%;
    }
    .main {
        margin: 35px;
        margin-top: 10px;
    }
    .inline {
        margin: 10px;
        margin-left: 0px;
        margin-right: 20px;
    }
</style>


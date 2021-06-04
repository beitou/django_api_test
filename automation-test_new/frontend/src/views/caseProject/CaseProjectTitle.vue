
<template>
    <div class="main">
        <el-row :span="24">
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{type}}</h1>
                    <div>用例类型</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '用例成员管理'}" style='text-decoration: none;color: #000000;'><h1><img src="../../assets/member.png" class="member">{{memberCount}}人</h1></router-link>
                    <div>项目组成员</div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :span="24">
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '用例列表'}" style='text-decoration: none;color: #000000;'><h1>{{caseCount}}条用例</h1></router-link>
                    <div>用例数量</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '用例需求列表'}" style='text-decoration: none;color: #000000;'><h1>{{requirementCount}}个需求</h1></router-link>
                    <div>需求数量</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '用例项目动态'}" style='text-decoration: none;color: #000000;'><h1>{{dynamicCount}}条动态</h1></router-link>
                    <div>用例项目三天内动态</div>
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
                    <h1>{{updateDate}}</h1>
                    <div>最近更新时间</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{createDate}}</h1>
                    <div>创建时间</div>
                </el-card>
            </el-col>
            <el-col :span="6" class='inline'>
                <el-card class="box-card">
                    <h1>{{version}}</h1>
                    <div>版本</div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import { getCaseProjectDetail } from '../../api/api'
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
                requirementCount: '0',
            }
        },
        methods: {
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
                            self.createDate = data.createTime;
                            self.requirementCount = data.requirementCount;
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
            this.getCaseProjectInfo()
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


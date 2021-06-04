<template>
    <section>
        <router-link :to="{ name: '用例列表', params: {caseProject_id: this.$route.params.caseProject_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>用例列表</el-button>
        </router-link>
        <el-radio-group v-model="radio" style="margin-left: 50px">
            <router-link @click.native="showNavi('用例基础信息')" :to="{ name: '用例基础信息', params: { caseProject_id: this.$route.params.caseProject_id, case_id: this.$route.params.case_id}}" style='text-decoration:none;'>
                <el-radio-button label="用例基础信息">
                    <div style="width: 80px">用例基础信息</div>
                </el-radio-button>
            </router-link>
            <router-link @click.native="showNavi('用例历史')" :to="{ name: '用例历史', params: { caseProject_id: this.$route.params.caseProject_id, case_id: this.$route.params.case_id}}" style='text-decoration:none;'>
                <el-radio-button label="用例历史">
                    <div style="width: 80px">用例历史</div>
                </el-radio-button>
            </router-link>
            <router-link @click.native="showNavi('修改用例')" :to="{ name: '修改用例', params: { caseProject_id: this.$route.params.caseProject_id, case_id: this.$route.params.case_id}}" style='text-decoration:none;'>
                <el-radio-button label="修改用例">
                    <div style="width: 80px">修改用例</div>
                </el-radio-button>
            </router-link>
            <el-radio-button label="删除" @click.native="handleDel">
                <div style="width: 80px">删除</div>
            </el-radio-button>
        </el-radio-group>
        <div style="margin-left: 10px;margin-right: 20px">
            <router-view></router-view>
        </div>
    </section>
</template>

<script>
    import { delCase } from '../../../api/api'
    import $ from 'jquery'
    export default {
        name: "api-form",
        data() {
            return {
                radio: "",
            }
        },
        methods: {
            handleDel: function () {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        caseProject_id: Number(this.$route.params.caseProject_id),
                        ids: this.$route.params.case_id,
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                    delCase(headers, params).then(_data => {
                        let { msg, code, data } = _data;
                        if (code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getCaseList()
                    });
                });
            },
            showNavi(title) {
                this.radio = title
            }
        },
        mounted() {
            this.radio = this.$route.name
        }
    }

</script>

<style lang="scss" scoped>
    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
    .head-class {
        font-size: 17px
    }
    .parameter-a {
        display: block;
    }
    .parameter-b {
        display: none;
    }
    .selectInput {
        position: absolute;
        /*margin-left: 7px;*/
        padding-left: 9px;
        width: 180px;
        /*border-radius:0px;*/
        /*height: 38px;*/
        left: 1px;
        border-right: 0px;
    }
</style>
<style lang="scss">
    .selectInput{
        input{
            border-right: 0px;
            border-radius: 4px 0px 0px 4px;
        }
    }
</style>
<template>
    <section>
        <router-link :to="{ name: '用例需求列表', params: {caseProject_id: this.$route.params.caseProject_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>用例需求列表</el-button>
        </router-link>
        <strong class="title" style="margin-left: 20px; font-size: 18px">{{this.titleName}}</strong>
        <el-radio-group v-model="radio" style="margin-left: 30px">
            <router-link @click.native="showNavi('需求基础信息')" :to="{ name: '需求基础信息', params: { caseProject_id: this.$route.params.caseProject_id, caseRequirement_id: this.$route.params.caseRequirement_id}}" style='text-decoration:none;'>
                <el-radio-button label="需求基础信息">
                    <div style="width: 80px">需求基础信息</div>
                </el-radio-button>
            </router-link>
            <router-link @click.native="showNavi('Bug详情')" :to="{ name: 'Bug详情', params: { caseProject_id: this.$route.params.caseProject_id, caseRequirement_id: this.$route.params.caseRequirement_id, zenTao_id: this.zentao_id }}" style='text-decoration:none;'>
                <el-radio-button label="Bug详情">
                    <div style="width: 80px">Bug详情</div>
                </el-radio-button>
            </router-link>
            <router-link @click.native="showNavi('邮件发送')" :to="{ name: '邮件发送', params: { caseProject_id: this.$route.params.caseProject_id, caseRequirement_id: this.$route.params.caseRequirement_id}}" style='text-decoration:none;'>
                <el-radio-button label="邮件发送">
                    <div style="width: 80px">邮件发送</div>
                </el-radio-button>
            </router-link>
        </el-radio-group>
        <div style="margin-left: 10px;margin-right: 20px">
            <router-view></router-view>
        </div>
    </section>
</template>

<script>
    import { getCaseRequirement } from '../../../api/api'
    import $ from 'jquery'
    export default {
        name: "api-form",
        data() {
            return {
                radio: "",
                titleName: "",
                zentao_id:"",
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
                        self.titleName = data.data[0].name;
                        self.zentao_id = data.data[0].zentao_id;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            showNavi(title) {
                this.radio = title
            }
        },
        mounted() {
            this.radio = this.$route.name;
            this.getRequirement();
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
<template>
    <section>
        <router-link :to="{ name: '用例列表', params: {caseProject_id: this.$route.params.caseProject_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>用例列表</el-button>
        </router-link>
        <router-link :to="{ name: '用例列表', params: {caseProject_id: this.$route.params.caseProject_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list" style="float: right">取消</el-button>
        </router-link>
        <el-button class="return-list" type="primary" style="float: right; margin-right: 15px" @click.native="addCaseInfo">保存</el-button>
        <el-form :model="form" ref="form" :rules="FormRules">
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;">
                <el-row>
                    <el-col :span='10'>
                        <el-form-item label="需求列表:" prop="caseRequirement_id">
                            <el-select v-model="form.caseRequirement_id" placeholder="请选择需求">
                                <el-option v-for="(item,index) in requirement.data" :key="index+''" :label="item.name" :value="item.id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span='10'>
                        <el-form-item label="优先级:" prop="priority">
                            <el-select v-model="form.priority" placeholder="请选择优先级">
                                <el-option v-for="(item,index) in priority" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="测试阶段:" prop="stageList">
                            <el-checkbox-group v-model.trim="form.stageList" @change="handleCheckChange">
                                <el-checkbox v-for="(item,index) in stageList" :key="index+''" :label="item.value" :value="item.value" >{{ item.label }}</el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="用例名称:" prop="name">
                            <el-input v-model.trim="form.name" placeholder="用例名称" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="测试类型:" prop="testType">
                            <el-input v-model.trim="form.testType" placeholder="测试类型" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="操作步骤:" prop="operationSteps" >
                            <el-input v-model.trim="form.operationSteps" type="textarea" :rows="8" placeholder="操作步骤" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="预期结果:" prop="operationSteps" >
                            <el-input v-model.trim="form.expectedResults" type="textarea" :rows="8" placeholder="预期结果" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span='8'>
                        <el-form-item label="测试结果:" prop="actualResult">
                            <el-select v-model="form.actualResult" placeholder="请选择结果">
                                <el-option v-for="(item,index) in actualResult" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="原因:" prop="reason" >
                            <el-input v-model.trim="form.reason" placeholder="原因" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="版本:" prop="version" >
                            <el-input v-model.trim="form.version" placeholder="版本" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='24'>
                        <el-form-item label="硬件:" prop="hardware" >
                            <el-input v-model.trim="form.hardware" placeholder="硬件" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </div>
        </el-form>
    </section>
</template>
<script>
    import { addCase, getCaseRequirement } from "../../../api/api";

    export default {
        data: function () {
            return {
                priority: [{value: 'p1', label: 'P1'},
                    {value: 'p2', label: 'P2'},
                    {value: 'p3', label: 'P3'},
                    {value: 'p4', label: 'P4'}],
                actualResult: [{value: '0', label: '未执行'},
                    {value: '1', label: '通过'},
                    {value: '2', label: '失败'}],
                stageList: [{value: '0', label: '冒烟用例'},
                    {value: '1', label: '功能用例'},
                    {value: '2', label: '回归用例'}],
                requirement: [],
                isIndeterminate: true,
                checkAll: false,
                result: true,
                activeNames: ['1', '2', '3', '4'],
                id: "",
                parameterRaw: "",
                request3: true,
                form: {
                    reason: '',
                    version: '',
                    hardware: '',
                    stageList: ['1', '2'],
                    priority: 'p2',
                    caseRequirement_id: '',
                    name: '',
                    operationSteps: '',
                    expectedResults: '',
                    actualResult: '0',
                    testType: '',
                },
                FormRules: {
                    priority: [{required: true, message: '请选择优先级', trigger: 'blur'}],
                    name: [{required: true, message: '请输入名称', trigger: 'blur'}],
                    caseRequirement_id: [{required: true, message: '请选择需求', trigger: 'blur'}],
                    operationSteps: [{required: true, message: '请输入操作步骤', trigger: 'blur'}],
                    expectedResults: [{required: true, message: '请输入预期结果', trigger: 'blur'}],
                    actualResult: [{required: true, message: '请选择测试结果', trigger: 'blur'}],
                    stageList: [{required: true, message: '请选择测试阶段', trigger: 'blur'}],
                },
                editForm: {
                    name: "",
                    value: "",
                    required: "",
                    restrict: "",
                    description: "",
                },
                // editLoading: false
            }
        },
        methods: {
            addCaseInfo: function () {
                this.$refs.form.validate((valid) => {
                    console.log(valid);
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            let _parameter = {};
                            console.log(_parameter)
                            let params = {
                                caseProject_id: Number(self.$route.params.caseProject_id),
                                caseRequirement_id: Number(self.form.caseRequirement_id),
                                name: self.form.name,
                                priority: self.form.priority,
                                operationSteps: self.form.operationSteps,
                                expectedResults: self.form.expectedResults,
                                actualResult: self.form.actualResult,
                                reason: self.form.reason,
                                version: self.form.version,
                                hardware: self.form.hardware,
                                testType: self.form.testType,
                                stage: self.form.stageList,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

                            };
                            addCase(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                if (code === '999999') {
                                    self.$router.push({
                                        name: '用例列表',
                                        query: {
                                            caseProject_id: self.$route.params.caseProject_id,
                                            requirement: self.form.caseRequirement_id
                                        }
                                    });
                                    self.$message({
                                        message: '保存成功',
                                        center: true,
                                        type: 'success'
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            })
                        })
                    }
                })
            },
            handleCheckChange(value) {
                let checkedCount = value.length;
                this.checkAll = checkedCount === this.form.stageList.length;
                this.isIndeterminate = checkedCount > 0 && checkedCount < this.form.stageList.length;
            },
            // 获取api分组
            getRequirement() {
                let self = this;
                let params = {
                    caseProject_id: this.$route.params.caseProject_id
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getCaseRequirement(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {
                        self.requirement = data;
                        self.form.caseRequirement_id = this.$route.query.caseRequirement;
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            onSubmit() {
                console.log('submit!');
            }
        },
        mounted() {
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

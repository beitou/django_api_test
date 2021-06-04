<template>
    <section>
        <!--工具条-->
        <el-col :span="24" style="height: 46px">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="getRequirement"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getRequirement">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="requirementAdd">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <!--列表-->
        <el-table :data="caseProject" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="id" label="编号" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="name" label="需求名称" min-width="45%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <router-link v-if="scope.row.name" :to="{ name: '需求用例列表', params: {caseProject_id: $route.params.caseProject_id, caseRequirement_id: scope.row.id}}" style='text-decoration: none;'>
                        {{ scope.row.name }}
                        <el-badge :value="scope.row.caseRequirementCount" type="primary" ></el-badge>
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column prop="user" label="创建人" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column label="操作" min-width="15%">
                <template slot-scope="scope" style="margin-top: 10px">
                    <router-link v-if="scope.row.name" :to="{ name: '需求基础信息', params: {caseProject_id: $route.params.caseProject_id, caseRequirement_id: scope.row.id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="small" size="small">详情</el-button>
					</router-link>
                    <el-button type="primary" icon="el-icon-edit" circle size="small" @click="handleEdit(scope.$index, scope.row)"></el-button>
                    <el-button type="danger" icon="el-icon-delete" circle size="small" @click="handleDel(scope.$index, scope.row)" style="margin-left:0px;"></el-button>
                    <!--<el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>-->
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>

        <!--编辑界面-->
        <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 80%; left: 10%">
            <el-form :model="editForm"  :rules="editFormRules" ref="editForm" label-width="80px">
                <el-form-item label="需求名称" prop='name'>
                    <el-input type="textarea" :rows="5" v-model.trim="editForm.name"></el-input>
                </el-form-item>
                <el-form-item label="蝉道ID" prop='zentao_id'>
                    <el-input type="textarea" :rows="1" v-model.trim="editForm.zentao_id"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 80%; left: 10%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-form-item label="需求名称" prop='name'>
                    <el-input type="textarea" :rows="5" v-model.trim="addForm.name"></el-input>
                </el-form-item>
                <el-form-item label="蝉道ID" prop='zentao_id'>
                    <el-input type="textarea" :rows="1" v-model.trim="addForm.zentao_id"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>
    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import { getCaseRequirement, delCaseRequirement,
    updateCaseRequirement, addCaseRequirement} from '../../../api/api'
    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                caseProject: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                update: true,
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    name: [
                        { required: true, message: '请输入需求名称', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' },
                    ],
                },
                //编辑界面数据
                editForm: {
                    name: '',
                    zentao_id: '',
                },
                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    name: [
                        { required: true, message: '请输入需求名称', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '',
                    zentao_id: '0',
                }

            }
        },
        methods: {
            // 获取需求列表
            getRequirement() {
                this.listLoading = true;
                let self = this;
                let params = {
                    caseProject_id: this.$route.params.caseProject_id,
                    page: self.page,
                    name: self.filters.name
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getCaseRequirement(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.total = data.total;
                        self.caseProject = data.data
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        caseProject_id: Number(this.$route.params.caseProject_id),
                        ids: [row.id, ]
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                    delCaseRequirement(headers, params).then(_data => {
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
                        self.getRequirement()
                    });
                });
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getRequirement()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            requirementAdd: function () {
                this.addFormVisible = true;
            },
            //编辑
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                caseProject_id: Number(this.$route.params.caseProject_id),
                                id: Number(self.editForm.id),
                                name: self.editForm.name,
                                zentao_id: self.editForm.zentao_id,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            updateCaseRequirement(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getRequirement()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            })
                        });
                    }
                });
            },
            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    console.log(valid);
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = {
                                caseProject_id: Number(this.$route.params.caseProject_id),
                                name: self.addForm.name,
                                zentao_id: self.addForm.zentao_id,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            addCaseRequirement(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getRequirement()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getRequirement()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params = {
                        caseProject_id: Number(this.$route.params.caseProject_id),
                        ids: ids
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delCaseRequirement(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getRequirement()
                    })
                })
            },
        },
        mounted() {
            this.getRequirement();

        }
    }

</script>
<style>
</style>

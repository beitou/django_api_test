<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.name" placeholder="名称" @keyup.enter.native="getScriptList"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="getScriptList">查询</el-button>
                </el-form-item>
                <el-form-item>

                    <el-form-item>
                        <el-button type="primary" @click="handleAdd">新增</el-button>
                    </el-form-item>

                </el-form-item>

                <!--<el-form-item>-->
                    <!--<el-dropdown split-button type="primary" @click="handleAddGroup">-->
                        <!--增加分类-->
                        <!--<el-dropdown-menu slot="dropdown">-->
                            <!--<template v-for="item in groupData">-->
                                <!--<el-dropdown-item @click.native="handleCommand(item)">-->
                                    <!--{{item}}-->
                                <!--</el-dropdown-item>-->
                            <!--</template>-->
<!--<el-dropdown-item @click.native="handleCommand(item)" divided>编辑</el-dropdown-item>-->
                        <!--</el-dropdown-menu>-->

                    <!--</el-dropdown>-->

                <!--</el-form-item>-->
            </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="script" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;"
        >
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="name" label="脚本名称" min-width="20%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link v-if="scope.row.status" :to="{ name: '脚本查看', params: {script_id: scope.row.id}}"
                                 style='text-decoration: none;color: #000000;'>
                        {{ scope.row.name }}
                    </router-link>
                    {{ !scope.row.status?scope.row.name:""}}
                </template>
            </el-table-column>
            <el-table-column prop="description" label="脚本描述" min-width="12%" sortable>
            </el-table-column>

            <el-table-column prop="LastUpdateTime" label="最后修改时间" min-width="16%" sortable>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="9%" sortable>
                <template slot-scope="scope">
                    <img v-show="scope.row.status" src="../../assets/icon-yes.svg"/>
                    <img v-show="!scope.row.status" src="../../assets/icon-no.svg"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="20%">
                <template slot-scope="scope">
                    <router-link :to="{ name: '编辑脚本', params: {script_id: scope.row.id}}"
                                 style='text-decoration: none;color: #000000;'>
                        <el-button size="small">编辑</el-button>
                    </router-link>
                    <el-button type="success" size="small" @click="scriptRun(scope.$index, scope.row)"
                               v-loading.fullscreen.lock="fullscreenLoading"

                    >运行
                    </el-button>

                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>

                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20"
                           :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>

        <!--新增-->
        <el-dialog title="脚本类型编辑" :visible.sync="addGroupFormVisible" :close-on-click-modal="false"
                   style="width: 60%; left: 20%">
            <el-form :model="addGroupForm" label-width="80px" :rules="addGroupFormRules" ref="addGroupForm">
                <el-form-item label="分组名称" prop='firstgroup'>
                    <el-input v-model.trim="addGroupForm.firstgroup" auto-complete="off"
                              style="width: 90%"></el-input>
                </el-form-item>
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addGroupFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addGroupSubmit" :loading="addGroupLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false"
                   style="width: 75%; left: 12.5%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-form-item label="脚本名称" prop="name">
                    <el-input v-model.trim="addForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-row :gutter="24">
                    <el-col :span="12">
                        <el-form-item label="脚本分类" prop='type'>
                            <el-input v-model.trim="addForm.type" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <!--<el-col :span="12">-->
                    <!--<el-form-item label="版本号" prop='version'>-->
                    <!--<el-input v-model.trim="addForm.version" auto-complete="off"></el-input>-->
                    <!--</el-form-item>-->
                    <!--</el-col>-->
                </el-row>
                <el-form-item label="脚本描述" prop='description'>
                    <el-input type="textarea" :rows="6" v-model="addForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>

        <el-dialog
                :title="resultTitle"
                :visible.sync="dialogVisible"
                width="60%">
            <el-input
                    type="textarea"
                    :readonly="true"
                    :autosize="{ minRows: 2, maxRows: 10}"
                    placeholder=""
                    v-model="resultData">
            </el-input>
            <!--<span>-->
            <!--{{resultData}}</span>-->
            <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
  </span>
        </el-dialog>
    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import {
        updateProject, addScript, getScriptList, delScript, runScript, addScriptGroup, scriptGroupList, delScriptGroup
    } from '../../api/api';
    import {Loading} from 'element-ui';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                options: {
                    fullscreen: true,
                    text: '脚本执行中',
                    background: 'rgba(0, 0, 0, 0.8)',
                },
                filters: {
                    name: ''
                },
                script: [],
                total: 0,
                page: 1,
                dialogVisible: false,
                listLoading: false,
                addGroupFormVisible: false,
                addGroupLoading: false,
                addGroupFormRules: {
                    firstgroup: [
                        {required: true, message: '请输入分类名称', trigger: 'blur'},
                        // { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    ]
                },
                groupData: ['a', 'b', 'c'],
                //新增界面数据
                addGroupForm: {
                    firstgroup: '',
                },
                resultData: '未获得执行结果',
                resultTitle: '未获得执行job信息',
                sels: [],//列表选中列


                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    name: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                        {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}
                    ],
                    type: [
                        {required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    // version: [
                    //     { required: true, message: '请输入版本号', trigger: 'blur' },
                    //     { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    // ],
                    description: [
                        {required: true, message: '请输入描述信息', trigger: 'blur'},
                        {max: 1024, message: '不能超过1024个字符', trigger: 'blur'}
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '',
                    version: '',
                    type: '',
                    description: ''
                }

            }
        },
        methods: {

            // 获取项目列表
            getScriptList() {
                this.listLoading = true;
                let self = this;
                let params = {page: self.page, name: self.filters.name};
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                getScriptList(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '999999') {
                        self.total = data.total;
                        self.script = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            getGroupList() {
                this.listLoading = true;
                let self = this;
                let params = {};
                let headers = {Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))};
                self.groupData=[];

                scriptGroupList(headers, params).then((res) => {
                    self.listLoading = false;
                    let {msg, code, data} = res;
                    if (code === '999999') {
                        data.forEach(
                            f => {
                                self.groupData.push(f.name);
                            }
                        );
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },

            handleCommand(command) {
                this.$message('click on item ' + command);
            },
            handleClick() {
                alert('button click');
            },
            scriptRun: function (index, row) {

                let self = this;


                let params = {
                    'script_id': row.id,
                    name:row.name,
                };
                let headers = {
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                runScript(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        /*self.total = data.total;
                        self.caseList = data.data;*/
                        self.resultData = data.resultCode;
                        self.resultTitle = row.name;
                        let loadingInstance = Loading.service(self.options);
                        loadingInstance.close();
                        self.dialogVisible = true;


                    } else {
                        self.fullscreenLoading = false;

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
                    let params = {ids: [row.id,]};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delScript(header, params).then(_data => {
                        let {msg, code, data} = _data;
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
                        self.getScriptList()
                    });
                })
            },

            handleCurrentChange(val) {
                this.page = val;
                this.getScriptList()
            },

            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
            },
            // 添加分组弹窗显示
            handleAddGroup() {
                this.addGroupFormVisible = true;
            },

            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                name: self.addForm.name,
                                type: self.addForm.type,
                                // version: self.addForm.version,
                                description: self.addForm.description
                            });
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addScript(header, params).then(_data => {
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
                                    self.getScriptList()
                                } else if (code === '999997') {
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
                                    self.getScriptList()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            // 添加分组
            addGroupSubmit: function () {
                this.$refs.addGroupForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addGroupLoading = true;
                            //NProgress.start();
                            let params = {
                                name: self.addGroupForm.firstgroup
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                            };
                            addScriptGroup(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addGroupLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addGroupForm'].resetFields();
                                    self.addGroupFormVisible = false;
                                    self.getGroupList();
                                    self.init()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['addGroupForm'].resetFields();
                                    self.addGroupFormVisible = false;
                                    self.getApiGroup();
                                    self.init()
                                }
                            })
                        });
                    }
                });
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: ids};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delScript(header, params).then(_data => {
                        let {msg, code, data} = _data;
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
                        self.getScriptList()
                    });
                })
            }
        },

        mounted() {
            this.getScriptList();
            this.getGroupList();
        }
    }

</script>

<style>

</style>
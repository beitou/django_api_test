<template>
    <el-row class="container">
        <el-col :span="24" class="header">
            <el-col :span="10" class="logo" :class="collapsed?'logo-collapse-width':'logo-width'">
                <router-link to="/Script" style='text-decoration: none;color: #FFFFFF;'>{{collapsed?'':sysName}}
                </router-link>
            </el-col>
            <el-col :span="4" class="userinfo">
                <el-dropdown trigger="hover">
                    <span class="el-dropdown-link userinfo-inner"><img
                            src="../../assets/userphoto.jpg"/> {{sysUserName}}</span>
                    <el-dropdown-menu slot="dropdown">
                        <!--<el-dropdown-item>我的消息</el-dropdown-item>-->
                        <!--<el-dropdown-item>设置</el-dropdown-item>-->
                        <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </el-col>
        </el-col>

        <el-col :span="23" style="margin: 20px;">

            <router-link :to="{ name: '脚本列表', params: {}}" style='text-decoration: none;color: aliceblue;'>
                <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>脚本列表
                </el-button>
            </router-link>
            <router-link :to="{ name: '脚本列表', params: {}}" style='text-decoration: none;color: aliceblue;'>
                <el-button class="return-list" style="float: right">取消</el-button>
            </router-link>
            <el-button class="return-list" type="primary" style="float: right; margin-right: 15px"
                       @click.native="scriptUpdate">保存
            </el-button>


            <el-form :model="form" ref="form" :rules="FormRules">

                <el-container>
                    <el-aside width="20%">
                        <el-form-item label="脚本上传:" prop="fileList">
                            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;margin-top: 10px;padding:15px">
                                <el-upload
                                        class="upload-demo"
                                        action=""
                                        :on-preview="handlePreview"
                                        :on-remove="handleRemove"
                                        :before-upload="beforeUpload"
                                        :before-remove="beforeRemove"
                                        :on-change="handleChange"
                                        multiple
                                        :http-request="uploadFiles"
                                        :on-error="errorUpload"
                                        :file-list="form.fileList">
                                    <el-button size="small" type="primary">点击上传</el-button>
                                    <div slot="tip" class="el-upload__tip" style="text-align: left;margin-top: 20px">
                                        文件列表:
                                    </div>
                                </el-upload>
                            </div>
                        </el-form-item>
                        <el-form-item prop="executableFile">
                            <el-row style="text-align:left">
                                <el-col class="el-upload__tip" style="text-align:left;margin:10px"
                                        v-if="form.fileList.length>0">
                                    请选择脚本入口文件:
                                    <el-tooltip class="item" effect="dark"
                                                content="当job包含多个文件时，需要选择一个入口文件，每个job有且只能有一个入口文件"
                                                placement="right-start">
                                        <i class="el-icon-question"></i>
                                    </el-tooltip>
                                </el-col>
                                <div v-for="f in form.fileList" style="margin-left: 30px;">
                                    <el-col>
                                        <el-radio v-model="form.executableFile" :label="f.name">{{f.name}}</el-radio>
                                    </el-col>
                                </div>

                            </el-row>
                        </el-form-item>

                    </el-aside>
                    <el-container>


                        <el-header style="height: auto;margin-top: 20px; border: 1px;">
                            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;padding-bottom: 0px">
                                <el-row :gutter="40">
                                    <el-col :span="10">
                                        <el-form-item label="脚本名称:" prop="scriptName">

                                            <el-input v-model="form.scriptName" placeholder="请输入内容"></el-input>

                                        </el-form-item>
                                    </el-col>

                                    <el-col :span="10">
                                        <el-form-item label="脚本描述:" prop="description">
                                            <el-input v-model="form.description" placeholder="请输入内容"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </div>
                            <el-collapse v-model="activeNames">
                                <el-collapse-item style="text-align: left;" title="请求参数" name="1">
                                    <el-row :span="24">
                                        <el-table ref="multipleParameterTable" :data="form.parameter"
                                                  highlight-current-row

                                                  @selection-change="selsChangeParameter">
                                            <el-table-column type="selection" min-width="5%" label="头部">
                                            </el-table-column>
                                            <el-table-column prop="name" label="参数名" min-width="20%" sortable>
                                                <template slot-scope="scope">
                                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name"
                                                              placeholder="请输入参数值"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column prop="value" label="参数值" min-width="20%" sortable>
                                                <template slot-scope="scope">
                                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value"
                                                              placeholder="请输入参数值"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column prop="description" label="描述" min-width="20%" sortable>
                                                <template slot-scope="scope">
                                                    <el-input type="textarea" :rows="1"
                                                              v-model.trim="scope.row.description"
                                                              placeholder="请输入描述"></el-input>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="操作" min-width="7%">
                                                <template slot-scope="scope">
                                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;"
                                                       @click="delParameter(scope.$index)"></i>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="" min-width="10%">
                                                <template slot-scope="scope">
                                                    <el-button v-if="scope.$index===(form.parameter.length-1)"
                                                               size="mini"
                                                               class="el-icon-plus" @click="addParameter"></el-button>
                                                </template>
                                            </el-table-column>
                                            <el-table-column label="" min-width="18%"></el-table-column>
                                        </el-table>


                                    </el-row>
                                </el-collapse-item>
                            </el-collapse>
                        </el-header>

                        <el-main>

                            <el-form-item label="编辑文件名:" prop="editFileName">
                                <el-col :span="5">
                                    <el-input v-model="form.editFileName" placeholder="请输入文件名"></el-input>
                                </el-col>
                            </el-form-item>


                            <div v-show="1" class="raw" style="text-align:left;padding-bottom: 20px;">文件详情:
                                <el-button type="warning" style="float: right;position: relative;bottom: 5px;"
                                           @click.native="fileUpdate" round>更新文件
                                </el-button>
                            </div>

                            <div style="border: 1px solid #e6e6e6;text-align:left;">

                                <codemirror v-model="form.fileDetail" :options="cmOptions"></codemirror>

                            </div>
                            <!--</div>-->

                        </el-main>

                        <el-footer style="height:auto;text-align:right">
                            <el-button type="primary" style="float: right; margin-right: 15px;margin-left: 10px"
                                       @click.native="scriptRun" round :loading="scriptRunLoading">全部参数运行
                            </el-button>
                            <el-button type="success" @click.native="codeSubmit" round :loading="codeSubmitLoading ">选中参数运行</el-button>
                            <el-card class="box-card" style="margin-top:10px;">
                                <div v-show="1" class="raw" style="text-align:left;">展示执行结果</div>
                                <div v-model="form.resultData" v-show="1">
                                    <div style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden">

                                    </div>
                                    <el-input

                                            type="textarea"
                                            :readonly="true"
                                            :autosize="{ minRows: 2, maxRows: 10}"
                                            placeholder=""
                                            v-model="form.resultData">
                                    </el-input>
                                    <!--<pre id='resultHead'-->
                                    <!--style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden;text-align:left;font-size:1rem;color:#304455;">{{form.resultData}}-->
                                    <!--</pre>-->
                                </div>

                            </el-card>
                        </el-footer>
                    </el-container>
                </el-container>

            </el-form>
        </el-col>


    </el-row>
</template>

<script>
    import {
        uploadFile,
        getFileDetail,
        delFile,
        getScript,
        UpdateScript,
        runCode,
        runScript,
        updateFile
    } from '../../api/api';
    import "codemirror/theme/ambiance.css";
    import "codemirror/lib/codemirror.css";
    import "codemirror/addon/hint/show-hint.css";

    import {codemirror} from 'vue-codemirror'

    require("codemirror/mode/python/python.js");
    require('codemirror/addon/fold/foldcode.js');
    require('codemirror/addon/fold/foldgutter.js');
    require('codemirror/addon/fold/brace-fold.js');
    require('codemirror/addon/fold/xml-fold.js');
    require('codemirror/addon/fold/indent-fold.js');
    require('codemirror/addon/fold/markdown-fold.js');
    require('codemirror/addon/fold/comment-fold.js');

    export default {
        data() {
            var checkExecutableFile = (rule, value, callback) => {
                if (this.form.fileList.length > 1 && this.form.executableFile === '') {
                    callback(new Error('请选择可执行文件'));
                } else {
                    callback();
                }
            };
            var checkEditFile = (rule, value, callback) => {
                if (this.form.fileDetail !== '' && this.form.editFileName === '') {
                    callback(new Error('请输入文件名'));
                } else {
                    callback();
                }
            };
            var checkFileList = (rule, value, callback) => {
                if (this.form.fileDetail !== '' && this.form.editFileName !== '') {
                    callback();
                } else if (this.form.fileDetail === '' && this.form.editFileName === '' && this.form.fileList.length === 0) {
                    callback(new Error('请上传脚本文件'));
                } else {
                    callback();
                }
            };


            return {
                tabPosition: 'top',
                codeSubmitLoading:false,
                scriptRunLoading:false,
                script_id: '',
                sysName: '小帮规划质量控制中心',
                collapsed: false,
                sysUserName: '',
                sysUserAvatar: '',
                falg: '',
                activeNames: ['1'],
                executable: '',
                editor: '',
                multipleSelection: [{name: "", value: ""},

                ],
                ParameterTyep: true,
                cmOptions: {
                    // codemirror options
                    indentWithTabs: true,
                    smartIndent: true,
                    lineNumbers: true,
                    matchBrackets: true,
                    mode: 'python',
                    extraKeys: {'Command': 'autocomplete'},//自定义快捷键

                },
                form: {
                    fileList: [],
                    parameter: [{name: "", value: "", description: ""},

                    ],
                    executableFile: '',
                    scriptName: '',
                    description: '',
                    editFileName: '',
                    fileDetail: '',

                    resultData: '',


                },

                FormRules: {
                    fileList: [
                        // {required: true, message: '请上传脚本文件', trigger: 'blur'},
                        {validator: checkFileList, trigger: 'blur'},
                    ],

                    scriptName: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请输入描述', trigger: 'blur'},
                    ],
                    executableFile: [
                        {validator: checkExecutableFile, trigger: 'blur'},

                    ],
                    editFileName: [
                        {validator: checkEditFile, trigger: 'blur'},

                    ],

                },


            }
        },

        methods: {
            selsChangeParameter: function (sels) {
                this.multipleSelection = sels
            },
            fileUpdate: function () {
                let self = this;
                let params = {
                    'script_id': this.$route.params.script_id,
                    'fileName': self.form.editFileName,
                    'fileDetail': self.form.fileDetail,
                };
                let headers = {
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                updateFile(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {

                        self.$message({
                            message: '文件更新成功',
                            center: true,
                            type: 'success'
                        });
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            test: function () {
                console.log(this.form.fileList)
            },
            scriptUpdate: function () {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            let params = {
                                name: this.form.scriptName,
                                description: this.form.description,
                                scriptParams: this.form.parameter,
                                editFile: this.form.editFileName,
                                fileDetail: this.form.fileDetail,
                                executable: this.form.executableFile,
                                filelist: this.form.fileList,
                                script_id: this.$route.params.script_id,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

                            };
                            UpdateScript(headers, params).then(_data => {
                                let {msg, code, data} = _data;
                                if (code === '999999') {
                                    // self.$router.push({
                                    //     name: '脚本列表',
                                    //     params: {}
                                    // });
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


            uploadFiles(file) {


                let self = this;
                let flag = true;

                let params = new FormData();
                params.append('file', file.file);//传文件
                params.append('script_id', this.$route.params.script_id);

                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };

                if (flag) {
                    uploadFile(headers, params).then(_data => {
                        let {msg, code, data} = _data;
                        if (code === '999999') {

                            self.$message({
                                message: '文件上传成功',
                                center: true,
                                type: 'success'
                            });
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    })
                }

            },

            beforeRemove() {
                return this.$confirm(`确定移除？`);
            },


            handleRemove(file, fileList) {

                let name = {name: file.name};
                this.form.fileList.pop(name);
                let self = this;
                let params = {
                    "fileName": file.name,
                    'script_id': this.$route.params.script_id,
                };

                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                delFile(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {
                        self.$message({
                            message: '文件删除成功',
                            center: true,
                            type: 'success'
                        });
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })


            }
            ,
            handlePreview(file, fileList) {
                let self = this;

                let params = {
                    "fileName": file.name,
                    'script_id': this.$route.params.script_id,
                };

                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getFileDetail(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {

                        this.form.fileDetail = data.getFile.fileDetail;
                        this.form.editFileName = data.getFile.fileName;

                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            }
            ,
            handleChange(file, fileList) {

                let name = {name: file.name};
                this.form.fileList.push(name);

            },


            handleselect: function (a, b) {
            }
            ,
            onSubmit() {
                console.log('submit!');
            }
            ,

            addParameter() {
                let parameter = {name: "", value: ""};
                this.form.parameter.push(parameter);
                let rows = [this.form.parameter[this.form.parameter.length - 1]];
                this.toggleParameterSelection(rows)
            }
            ,
            toggleParameterSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleParameterTable.toggleRowSelection(row, true);
                });
            }
            ,
            delParameter(index) {
                if (this.form.parameter.length !== 1) {
                    this.form.parameter.splice(index, 1)
                }
            }
            ,
            beforeUpload(file) {
                // const res = this.form.fileList.some((item) => {
                //     return item.name === file.name
                // });
                // if (res) {
                //
                //     this.$message.warning(`这个文件已经上传过了`);
                //     return false;
                // }
            }
            ,
            //退出登录
            logout: function () {
                let _this = this;
                this.$confirm('确认退出吗?', '提示', {
                    //type: 'warning'
                }).then(() => {
                    sessionStorage.removeItem('token');
                    _this.$router.push('/login');
                }).catch(() => {

                });
            }
            ,
            showMenu(i, status) {
                this.$refs.menuCollapsed.getElementsByClassName('submenu-hook-' + i)[0].style.display = status ? 'block' : 'none';
            }
            ,
            codeSubmit: function () {

                let self = this;
                self.codeSubmitLoading=true;
                let params = {
                    code: self.form.fileDetail,
                    name: self.form.scriptName,
                    'parameter': self.multipleSelection,
                };
                let headers = {
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                runCode(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.codeSubmitLoading = false;
                    if (code === '999999') {
                        /*self.total = data.total;
                        self.caseList = data.data;*/
                        self.form.resultData = data.resultCode;
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            scriptRun: function () {
                let self = this;
                self.scriptRunLoading=true;
                let params = {
                    'script_id': this.$route.params.script_id,
                    name:self.form.scriptName,
                };
                let headers = {
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                runScript(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.scriptRunLoading = false;
                    if (code === '999999') {
                        /*self.total = data.total;
                        self.caseList = data.data;*/
                        self.form.resultData = data.resultCode;
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },

            getScriptInfo() {
                var self = this;
                let params = {script_id: this.$route.params.script_id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getScript(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.form.scriptName = data.name;
                        self.form.description = data.description;
                        self.form.parameter = data.parameter;
                        data.fileList.forEach(
                            f => {
                                let temp = {name: f.fileName};
                                self.form.fileList.push(temp);
                                if (f.executable === '1') {
                                    self.form.executableFile = f.fileName;
                                    self.form.editFileName = f.fileName;
                                    self.form.fileDetail = f.fileDetail;
                                }
                                console.log(f.fileName)
                            }
                        );

                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            }
            ,
        },
        mounted() {
            this.toggleParameterSelection(this.form.parameter);
            let user = sessionStorage.getItem('username');
            if (user) {
                name = JSON.parse(user);
                this.sysUserName = name || '';
            }
            this.getScriptInfo();

        }
    }

</script>

<style scoped lang="scss">
    @import '~scss_vars';

    .container {
        position: absolute;
        top: 0px;
        bottom: 0px;
        width: 100%;

        .header {
            height: 61px;
            line-height: 60px;
            background: $color-primary;
            color: #fff;

            .userinfo {
                text-align: right;
                padding-right: 35px;
                float: right;

                .userinfo-inner {
                    cursor: pointer;
                    color: #fff;

                    img {
                        width: 40px;
                        height: 40px;
                        border-radius: 20px;
                        margin: 10px 0px 10px 10px;
                        float: right;
                    }
                }
            }

            .logo {
                //width:230px;
                height: 60px;
                font-size: 20px;
                padding-left: 10px;
                padding-right: 10px;
                border-color: rgba(238, 241, 146, 0.3);
                border-right-width: 1px;
                border-right-style: solid;

                img {
                    width: 40px;
                    float: left;
                    margin: 10px 10px 10px 18px;
                }

                .txt {
                    color: #fff;
                }
            }

            .logo-width {
                width: 230px;
            }

            .logo-collapse-width {
                width: 60px
            }

            .tools {
                padding: 0px 23px;
                width: 14px;
                height: 60px;
                line-height: 60px;
                cursor: pointer;
            }
        }

        .title {
            width: 200px;
            float: left;
            color: #475669;
            font-size: 25px;
            margin: 15px;
            margin-left: 35px;
            margin-bottom: 0px;
            font-family: PingFang SC;
        }
    }

    .el-header {
        /*background-color: #B3C0D1;*/
        /*color: #333;*/
        text-align: left;
        /*line-height: 20px;*/
        margin-top: 20px;

    }

    .el-footer {
        /*background-color: #B3C0D1;*/
        /*color: #333;*/
        /*text-align: left;*/
        /*line-height: 20px;*/
        margin-top: 0px;

    }

    .el-aside {
        background-color: #D3DCE6;
        color: #333;
        text-align: left;
        line-height: 10px;
    }

    .el-main {
        /*background-color: #E9EEF3;*/
        color: #333;
        text-align: center;
        /*line-height: 300px;*/
    }

    body > .el-container {
        margin-bottom: 40px;
    }

    .el-container:nth-child(5) .el-aside,
    .el-container:nth-child(6) .el-aside {
        line-height: 260px;
    }


    .el-container:nth-child(7) .el-aside {
        line-height: 320px;
    }

    .el-textarea__inner {
        height: 230px;
        color: rebeccapurple;
    }

    .testClass {
        -webkit-text-fill-color: red;
    }

    .codePython {
        font-size: 11pt;
        font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace, serif;
    }

    input:disabled, textarea {
        opacity: 1;
        -webkit-text-fill-color: red;
    }

    .parameter-a {
        display: block;
    }

    .parameter-b {
        display: none;
    }

</style>
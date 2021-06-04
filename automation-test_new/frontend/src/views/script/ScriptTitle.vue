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
                       @click.native="scriptAdd">保存
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
                                    :before-remove="beforeRemove"
                                    :on-change="handleChange"
                                    multiple
                                    :http-request="uploadFiles"
                                    :file-list="form.fileList">
                                <el-button size="small" type="primary">点击上传</el-button>
                                <div slot="tip" class="el-upload__tip" style="text-align: left;margin-top: 20px">文件列表:
                                </div>
                            </el-upload>
                        </div>
                        </el-form-item>
                        <el-row style="text-align:center">


                            <el-col class="el-upload__tip" style="text-align:left;margin:10px" v-if="form.fileList.length>0">
                                请选择脚本入口文件:
                            </el-col>
                            <div v-for="f in form.fileList">
                                <el-col>
                                    <el-radio v-model="form.executableFile" :label="f.name">{{f.name}}</el-radio>
                                </el-col>
                            </div>

                        </el-row>

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
                                                    <el-input type="textarea" :rows="7" v-model.trim="scope.row.description" placeholder="请输入描述"></el-input>
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
                            <el-form-item label="文件详情:">
                                <el-input
                                        type="textarea"
                                        :rows="10"
                                        placeholder="请输入内容"
                                        v-model="scriptDtail"
                                        style="font-size:1rem;color:#304455;"
                                >
                                </el-input>
                            </el-form-item>
                        </el-main>
                        <el-footer style="height:auto;text-align:right">
                            <el-button type="success" round>试运行</el-button>
                            <el-card class="box-card" style="margin-top:10px;">
                                <div v-show="1" class="raw" style="text-align:left;">展示执行结果</div>
                                <div v-model="form.resultData" v-show="1">
                                    <div style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden">

                                    </div>
                                    <pre id='resultHead'
                                         style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden;text-align:left;font-size:1rem;color:#304455;">{{form.resultData}}
                                </pre>
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
    import {uploadFile, getFileDetail,addScript} from '../../api/api';

    export default {
        data() {
            return {
                tabPosition: 'top',
                project_id: '',
                sysName: '小帮规划质量控制中心',
                collapsed: false,
                sysUserName: '',
                sysUserAvatar: '',

                parameter: [{name: "", value: "", required: "", restrict: "", description: ""},

                ],
                activeNames: ['1', '2', '3', '4'],
                executable: '',
                form: {
                    fileList: [],
                    parameter: [{name: "", value: "", description: ""},

                    ],
                    executableFile: '',
                    scriptName: '',
                    description: '',
                    editFileName:'',
                    scriptDtail: '',

                    resultData: '',


                },
                FormRules: {
                    fileList:[
                        {required: true, message: '请上传脚本文件', trigger: 'blur'},
                    ],

                    scriptName: [
                        {required: true, message: '请输入名称', trigger: 'blur'},
                    ],
                    description: [
                        {required: true, message: '请输入描述', trigger: 'blur'},
                    ],

                },


            }
        },
        methods: {
            scriptAdd: function () {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            let params = {
                                name:this.form.scriptName,
                                description: this.form.description,
                                scriptParams:this.form.parameter,
                                editFile:this.form.editFileName,
                                scriptDtail:this.form.scriptDtail,
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

                            };
                            addScript(headers, params).then(_data => {
                                        let {msg, code, data} = _data;
                                        if (code === '999999') {
                                            // self.$router.push({name: '分组接口列表',
                                            //     params: {
                                            //         project_id: self.$route.params.project_id,
                                            //         firstGroup: self.form.apiGroupLevelFirst_id
                                            //     }
                                            // });
                                            self.$message({
                                                message: '保存成功',
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
                                    })
                        })
                    }
                })

            },


            uploadFiles(file) {


                let self = this;

                let params = new FormData();
                params.append('file', file.file);//传文件

                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                uploadFile(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {

                        console.log("123")
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },

            handleRemove(file, fileList) {
                let name = {name: file.name};
                this.form.fileList.pop(name);
                console.log(this.form.fileList);
            },
            handlePreview(file, fileList) {
                console.log(file);
                console.log(fileList);
                let self = this;

                let params = {
                    "fileName": file.name,
                };

                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getFileDetail(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    if (code === '999999') {

                        this.scriptDtail = data.data
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            handleChange(file, fileList) {
                // fileList.forEach(
                //     f=>{
                //         this.form.fileList.push(f.name);
                //     }
                // );
                if (file.name.length>0){
                    let name = {name: file.name};
                    this.form.fileList.push(name);
                }
                console.log(this.form.fileList);
                // this.fileList=[{}];
            },

            handleselect: function (a, b) {
            },
            onSubmit() {
                console.log('submit!');
            },

            addParameter() {
                let parameter = {name: "", value: ""};
                this.form.parameter.push(parameter);
                let rows = [this.form.parameter[this.form.parameter.length - 1]];
                this.toggleParameterSelection(rows)
            },
            toggleParameterSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleParameterTable.toggleRowSelection(row, true);
                });
            },
            delParameter(index) {
                if (this.form.parameter.length !== 1) {
                    this.form.parameter.splice(index, 1)
                }
            },
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
            },
            showMenu(i, status) {
                this.$refs.menuCollapsed.getElementsByClassName('submenu-hook-' + i)[0].style.display = status ? 'block' : 'none';
            },
        },
        mounted() {
            this.toggleParameterSelection(this.form.parameter);
            let user = sessionStorage.getItem('username');
            if (user) {
                name = JSON.parse(user);
                this.sysUserName = name || '';
//				this.sysUserAvatar = '../assets/user.png';
            }
            this.project_id = this.$route.params.project_id
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
    }


</style>
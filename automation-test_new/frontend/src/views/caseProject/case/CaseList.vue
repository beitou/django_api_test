<template>
	<section>
		<!--工具条-->
		<el-col :span="24" style="height: 46px">
			<el-form :inline="true" :model="filters" @submit.native.prevent>
				<el-form-item>
					<el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="getCaseList"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="getCaseList">查询</el-button>
				</el-form-item>
				<el-form-item>
					<router-link :to="{ name: '新增用例', query: {caseRequirement: this.$route.params.caseRequirement_id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="primary">新增</el-button>
					</router-link>
				</el-form-item>
				<!--<el-form-item>
					<el-button type="primary" @click.native="DownloadApi">下载用例文档</el-button>
				</el-form-item>-->
				<el-form-item>
					<el-button type="primary" @click.native="loadCaseFromExcel = true">导入测试用例</el-button>
					<el-dialog title="导入测试用例" :visible.sync="loadCaseFromExcel" :close-on-click-modal="false">
						<el-input v-model.trim="requirementName" placeholder="请输入需求名称" style="margin-bottom:10px;"></el-input>
						<el-input v-model.trim="zentao_id" placeholder="请输入蝉道id" style="margin-bottom:10px;"></el-input>
						<el-upload style="margin-bottom:10px;"
						  class="upload-demo"
						  drag
						  :limit="1"
						  :file-list="fileList"
						  :http-request="handleChange"
						  multiple>
						  <i class="el-icon-upload"></i>
						  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
						</el-upload>
						<el-button type="primary" @click="improtCaseData" :loading="addLoading">导入</el-button>
						<P v-if="!file || !requirementName" style="color: red; margin: 0px">需求名称和文件不能为空</P>
					</el-dialog>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click.native="caseExportExcel = true">导出测试用例</el-button>
						<el-dialog title="导出测试用例" :visible.sync="caseExportExcel" :close-on-click-modal="false">
						<el-input v-model.trim="requirementId" placeholder="请输入需求ID" style="margin-bottom:10px;"></el-input>
						<el-button type="primary" @click="DownloadApi" :loading="exportLoading">导出</el-button>
						<P v-if="!requirementId" style="color: red; margin: 0px">需求ID不能为空</P>
					</el-dialog>
				</el-form-item>
			</el-form>
		</el-col>
		<el-dialog title="修改所属需求" :visible.sync="updateGroupFormVisible" :close-on-click-modal="false" style="width: 60%; left: 20%">
			<el-form :model="updateGroupForm" label-width="80px" :rules="updateGroupFormRules" ref="updateGroupForm">
				<el-form-item label="需求名称" prop="firstGroup">
					<el-select v-model="updateGroupForm.firstGroup" placeholder="请选择">
						<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="updateGroupFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="updateGroupSubmit" :loading="updateGroupLoading">提交</el-button>
			</div>
		</el-dialog>

		<!--列表-->
		<el-table :data="caseList" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" min-width="5%">
			</el-table-column>
			<el-table-column prop="id" label="id" min-width="6%" sortable show-overflow-tooltip>
			</el-table-column>
            <el-table-column prop="stage" :formatter="stagFormat" label="阶段" min-width="7%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="name" label="用例名称" min-width="38%" sortable show-overflow-tooltip>
				<template slot-scope="scope">
					<el-icon name="name"></el-icon>
					<router-link :to="{ name: '用例基础信息', params: {case_id: scope.row.id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
				</template>
			</el-table-column>
			<el-table-column prop="userUpdate" label="更新人" min-width="7%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="lastUpdateTime" label="最近更新时间" min-width="12%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="actualResult" :formatter="actualResultFormat" label="用例状态" min-width="8%" sortable show-overflow-tooltip>
			</el-table-column>
			<el-table-column label="操作" min-width="17%">
				<template slot-scope="scope">
					<el-button type="small" size="small" @click="passCase(scope.$index, scope.row)">通过</el-button>
					<el-button type="small" size="small" @click="failCase(scope.$index, scope.row)" style="margin-left:0px">失败</el-button>
					<router-link :to="{ name: '修改用例', params: {case_id: scope.row.id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="primary" icon="el-icon-edit" circle size="small"></el-button>
					</router-link>
					<el-button type="danger" icon="el-icon-delete" circle size="small" @click="handleDel(scope.$index, scope.row)"></el-button>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button @click="batchPass" :disabled="this.sels.length===0">批量通过</el-button>
			<el-button @click="batchFail" :disabled="this.sels.length===0">批量失败</el-button>
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :page-count="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
	//import NProgress from 'nprogress'
    import { getCase, delCase, updateCase, importCase, ExportCaseExcel } from '../../../api/api'
	export const test = process.env.BASE_API;
    import $ from 'jquery'
	// import ElRow from "element-ui/packages/row/src/row";
    export default {
		// components: {ElRow},
		data() {
			return {
				filters: {
					name: ''
				},
				caseList: [],
				total: 0,
				page: 1,
				listLoading: false,
				sels: [],//列表选中列
				updateGroupFormVisible: false,
				updateGroupForm: {
					firstGroup: "",
				},
				updateGroupFormRules: {
					firstGroup: [{type: 'number', required: true, message: '请选择分组', trigger: 'blur'}],
				},
				group: [],
				updateGroupLoading: false,
				update: true,
				loadSwaggerApi: false,
				addLoading: false,
				loadCaseFromExcel: false,
				caseExportExcel: false,
				exportLoading: false,
				//新增界面数据
				requirementId: "",
				requirementName: "",
				zentao_id: "0",
				fileList: [],
				fileUrl: "",
				file: "",
			}
		},
		methods: {
			// 获取接口列表
			getCaseList() {
				this.listLoading = true;
				let self = this;
				let params = {
					caseProject_id: this.$route.params.caseProject_id,
					page: self.page,
					name: self.filters.name,
					caseRequirement_id: this.$route.params.caseRequirement_id,
				};
				let headers = {
					Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
				};
				getCase(headers, params).then(_data => {
					let {msg, code, data} = _data;
					self.listLoading = false;
					if (code === '999999') {
						self.total = data.total;
						self.caseList = data.data;
					} else {
						self.$message.error({
							message: msg,
							center: true,
						})
					}
				});
			},
			passCase: function (index, row) {
				let self = this;
				this.$confirm('确认通过吗？', '提示', {}).then(() => {
					let _parameter = {};
					console.log(_parameter)
					let params = {
						caseProject_id: Number(self.$route.params.caseProject_id),
						caseRequirement_id: Number(row.caseRequirement),
						actualResult: 1,
						name: row.name,
						operationSteps: row.operationSteps,
						expectedResults: row.expectedResults,
						stage: row.stage,
						id: row.id,
					};
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

					};
					updateCase(headers, params).then(_data => {
						let {msg, code, data} = _data;
						if (code === '999999') {
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
						self.getCaseList()
					});
				});
			},
			handleChange(file) {

				this.file = file;

			},
			failCase: function (index, row) {
				let self = this;
				this.$confirm('确认通过吗？', '提示', {}).then(() => {
					let _parameter = {};
					console.log(_parameter);
					let params = {
						caseProject_id: Number(self.$route.params.caseProject_id),
						caseRequirement_id: Number(row.caseRequirement),
						actualResult: 2,
						name: row.name,
						operationSteps: row.operationSteps,
						expectedResults: row.expectedResults,
						stage: row.stage,
						id: row.id,
					};
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

					};
					updateCase(headers, params).then(_data => {
						let {msg, code, data} = _data;
						if (code === '999999') {
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
						self.getCaseList()
					});
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
						ids: [row.id,]
					};
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
					};
					delCase(headers, params).then(_data => {
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
						self.getCaseList()
					});
				});
			},
			// 下载接口文档
            /*DownloadApi() {
                $.ajax({
                    type: "get",
                    url: test+"/api/api/Download",
                    async: true,
                    data: { caseProject_id: this.$route.params.caseProject_id},
                    headers: {
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    },
                    timeout: 5000,
                    success: function(data) {
                        if (data.code === "999999") {
                            window.open(test+"/api/api/download_doc?url="+data.data)
                        }
                    },
                })
            },*/
			// 翻页
            /*handleCurrentChange(val) {
                this.page = val;
                this.getApiList()
            },
            selsChange: function (sels) {
                if (sels.length>0) {
                    this.sels = sels;
                    this.update = false
                } else {
                    this.update = true
                }
            },*/
            actualResultFormat(row, column) {
				//return "为什么没有值！";
            	if (row.actualResult === '0') {
				  return "未执行";
				} else if (row.actualResult === '1') {
				  return "通过";
				} else if (row.actualResult === '2') {
				  return "失败";
				}
			  },
            stagFormat(row, column) {
                let str = [];
                if (row.stage.indexOf('0') !== -1) {
                    str = str + "冒 ";
                }
                if (row.stage.indexOf('1') !== -1) {
				  str = str + "功 ";
				}
                if (row.stage.indexOf('2') !== -1) {
				  str = str + "回";
				}
                return str;
            },
			// 下载接口文档
            DownloadApi() {
            	let self = this;
				let params = {
					caseProject_id: this.$route.params.caseProject_id,
					caseRequirement_id: this.requirementId,
				};
				let headers = {
					Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
				};
				ExportCaseExcel(headers, params).then(_data => {
					let {msg, code, data} = _data;
					if (code === '999999') {
						window.open(test + "/api/api/download_doc?url=" + data);
						self.exportLoading = false;
						self.caseExportExcel = false;
						self.getCaseList();
					} else {
						self.$message.error({
							message: msg,
							center: true,
						})
					}
				});
            },
			improtCaseData: function () {
				this.addLoading = true;
				if (this.file) {
					let self = this;
					let params = new FormData();
					params.append('caseProject_id', this.$route.params.caseProject_id);
					params.append('requirementName', String(this.requirementName));
					params.append('zentao_id', this.zentao_id);
					params.append('file', this.file.file);
					console.log(params);
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
					};
					importCase(headers, params).then(_data => {
						let {msg, code, data} = _data;
						if (code === '999999') {
							self.$message({
								dangerouslyUseHTMLString: true,
								message: msg,
								center: true,
								type: 'success'
							});
							self.loadCaseFromExcel = false;
							self.addLoading = false;
							self.getCaseList()
						} else {
							self.$message.error({
								dangerouslyUseHTMLString: true,
								message: msg,
								center: true,
							});
							self.loadCaseFromExcel = false;
							self.addLoading = false;
							self.getCaseList();
						}
					});
				}
			},
			// 翻页
            handleCurrentChange(val) {
                this.page = val;
                this.getCaseList()
            },
			selsChange: function (sels) {
				this.sels = sels;
                console.log(sels);
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
                    delCase(headers, params).then(_data => {
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
                        self.getCaseList()
                    })
                })
            },
			//批量通过
			batchPass: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认通过选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    let _parameter = {};
					console.log(_parameter)
					let params = {
						caseProject_id: Number(self.$route.params.caseProject_id),
						//caseRequirement_id: Number(row.caseRequirement),
						actualResult: 1,
						//name: row.name,
						//operationSteps: row.operationSteps,
						//expectedResults: row.expectedResults,
						//stage: row.stage,
						ids: ids,
					};
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

					};
					updateCase(headers, params).then(_data => {
						let {msg, code, data} = _data;
						if (code === '999999') {
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
						self.getCaseList()
					});
				});
            },
            batchFail: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认通过选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    let _parameter = {};
					console.log(_parameter)
					let params = {
						caseProject_id: Number(self.$route.params.caseProject_id),
						//caseRequirement_id: Number(row.caseRequirement),
						actualResult: 2,
						//name: row.name,
						//operationSteps: row.operationSteps,
						//expectedResults: row.expectedResults,
						//stage: row.stage,
						ids: ids,
					};
					let headers = {
						"Content-Type": "application/json",
						Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

					};
					updateCase(headers, params).then(_data => {
						let {msg, code, data} = _data;
						if (code === '999999') {
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
						self.getCaseList()
					});
				});
            }
        },
        mounted() {
            this.getCaseList();

        }
    }
</script>

<style lang="scss" scoped>
	.api-title {
		padding: 15px;
		margin: 0px;
		text-align: center;
		border-radius:5px;
		font-size: 15px;
		color: aliceblue;
		background-color: rgb(32, 160, 255);
		//background-color: rgb(58, 58, 58);
		font-family: PingFang SC;
	}
	.group .editGroup {
		float:right;
	}
	.row-title {
		margin: 35px;
	}
	.addGroup {
		margin-top: 0px;
		margin-bottom: 10px;
		border-radius: 25px;
	}
	.api-view-a {
		margin-left: 15px;
		margin-right: 15px;
		display: block;
	}
	.api-view-b {
		margin-left: 15px;
		margin-right: 15px;
		display: none;
	}
</style>
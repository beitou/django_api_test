<template>
    <section>
        <el-row :gutter="20">
            <el-col :span="14">
                <div id="myChart" :style="{height: '400px'}"></div>
            </el-col>
            <!--<el-col :span="7">-->
            <!--<div id="singleTestChart" :style="{height: '400px'}"></div>-->
            <!--</el-col>-->
        </el-row>
        <el-row :gutter="20">
            <el-col :span="14">
                <div id="myFailChart" :style="{height: '400px'}"></div>
            </el-col>
        </el-row>
        <p style="padding-left: 50px;color:#999">*注<strong>: </strong>选择时间查询测试记录，默认查询7天内结果</p>
        <el-row>
            <el-col :span="15" style="padding-left: 50px;padding-bottom: 10px">
                请选择测试时间:
                <el-date-picker v-model="timeArray" type="datetimerange" :picker-options="pickerOptions2"
                                range-separator="   至   " start-placeholder="开始日期" end-placeholder="结束日期" align="right"
                                :default-time="['00:00:00', '23:59:59']"
                ></el-date-picker>
                <el-button type="primary" @click.native="getTestResult">查询</el-button>
            </el-col>
        </el-row>
        <div style="padding-left: 50px;width: 96%">
            <el-table :data="tableData" v-loading="listLoading" :row-style="tableRowStyle">
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form label-position="left" inline class="demo-table-expand">
                            <el-form-item label="名称: ">
                                <span>{{ props.row.name }}</span>
                            </el-form-item>
                            <el-form-item>
                            </el-form-item>
                            <el-form-item label="接口地址： ">
                                <span>{{ props.row.apiAddress }}</span>
                            </el-form-item>
                            <el-form-item label="请求方式： ">
                                <span>{{ props.row.requestType }}</span>
                            </el-form-item>
                            <el-form-item label="测试结果： ">
                                <span>{{ props.row.result }}</span>
                            </el-form-item>
                            <el-form-item>
                            </el-form-item>
                            <el-form-item label="请求头： ">
                                <span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{ props.row.header }}</span>
                            </el-form-item>
                            <el-form-item label="返回头： ">
                                <span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{props.row.responseHeader}}</span>
                            </el-form-item>
                            <el-form-item label="请求参数： ">
                                <span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{ props.row.parameter }}</span>
                            </el-form-item>
                            <el-form-item label="返回结果： ">
                                <span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{props.row.responseData}}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column type="index" label="#" width="100">
                </el-table-column>
                <el-table-column prop="name" label="接口名称" min-width="29" sortable show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="automationTestSchedule" label="计划名称" min-width="29%" sortable
                                 show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="apiAddress" label="请求地址" min-width="20%" sortable show-overflow-tooltip>
                </el-table-column>
                <el-table-column prop="examineType" label="校验方式" min-width="12%" sortable show-overflow-tooltip>
                    <template slot-scope="scope">
                        <a v-if="scope.row.examineType === 'no_check'">不校验</a>
                        <a v-if="scope.row.examineType === 'only_check_status'">校验http状态</a>
                        <a v-if="scope.row.examineType === 'json'">JSON校验</a>
                        <a v-if="scope.row.examineType === 'entirely_check'">完全校验</a>
                        <a v-if="scope.row.examineType === 'Regular_check'">正则校验</a>
                    </template>
                </el-table-column>
                <el-table-column prop="result" label="结果" min-width="10%" :filters="resultFilter"
                                 :filter-method="filterHandler">
                    <template slot-scope="scope">
                        {{scope.row.result? scope.row.result: "NotRun"}}
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div style="margin-top: 5%"></div>
    </section>
</template>
<script>
    import echarts from 'echarts'
    import moment from "moment"
    import {getTestResultList, getTestTenResult} from '../../api/api'

    export default {
        data() {
            return {
                //测试报告信息
                scenario_data: [],
                test_scenario: [],//测试场景，用于图表的X轴
                //图表数据信息
                successTimes: [],
                failedTimes: [],
                successRatio: [],

                fail_data: [],
                fail_data_name: [],
                fail_data_count: [],

                //////////////////
                tableData: [],
                timeArray: [],
                listLoading: false,
                resultFilter: [
                    {text: 'ERROR', value: 'ERROR'},
                    {text: 'FAIL', value: 'FAIL'},
                    {text: 'NotRun', value: 'NotRun'},
                    {text: 'PASS', value: 'PASS'},
                ],
                time: "",
                elapsedTime: "",
                host: "",
                options: [],
                pass: "",
                fail: "",
                error: "",

                pickerOptions2: {
                    // disabledDate(time) {
                    //     return time.getTime() < Date.now() - 8.64e7;
                    // },
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 24 * 7);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 24 * 30);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 24 * 90);
                            picker.$emit('pick', [start, end]);
                        }
                    }],
                },

            }
        },

        mounted() {
            this.getdefault();
            this.getTestResult();
            // this.getLatelyTenTestResult();
        },
        methods: {
            getdefault() {
                var t = new Date();
                var t_y = t.getFullYear();
                var t_m = t.getMonth();
                var t_d = t.getDate();
                this.timeArray = [new Date(t_y, t_m, t_d - 7, 0, 0, 0), new Date(t_y, t_m, t_d, 23, 59, 59)]
            },
            getTestResult() {
                this.listLoading = true;
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id,
                    start_time: moment(this.timeArray[0]).format("YYYY-MM-DD HH:mm:ss"),
                    end_time: moment(this.timeArray[1]).format("YYYY-MM-DD HH:mm:ss"),
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                getTestResultList(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.listLoading = false;
                    if (code === '999999') {

                        self.scenario_data = data.scenario_data;
                        data.scenario_data.forEach((item) => {
                            self.test_scenario.push(item.scenario_name);
                            self.successTimes.push(item.success_count);
                            self.failedTimes.push(item.fail_count);
                            self.successRatio.push(item.success_count / item.total_count);
                        });
                        if (self.test_scenario.length < 10) {
                            for (let i = 0; i < (10 - self.test_scenario.length); i++) {
                                self.test_scenario.push("")
                            }
                        }
                        self.fail_data = data.fail_data;
                        data.fail_data.forEach((item) => {
                            self.fail_data_name.push(item.api_name);
                            self.fail_data_count.push(item.api_count);

                        });
                        if (self.fail_data_name.length < 10) {
                            for (let i = 0; i < (10 - self.fail_data_name.length); i++) {
                                self.fail_data_name.unshift("");
                                self.fail_data_count.unshift("");
                            }
                        }
                        self.tableData = data.data;
                        self.drawLine();
                        self.drawFailLine();
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            // getTestResult() {
            //     this.listLoading = true;
            //     let self = this;
            //     let params = {
            //         project_id: this.$route.params.project_id,
            //         time: this.time.toString()
            //     };
            //     let headers = {
            //         "Content-Type": "application/json",
            //         Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
            //     };
            //     getTestResultList(headers, params).then(_data => {
            //         let {msg, code, data} = _data;
            //         self.listLoading = false;
            //             if (code === '999999') {
            //                 self.total = data.total;
            //                 self.pass = data.pass;
            //                 self.fail = data.fail;
            //                 self.not_run = data.NotRun;
            //                 self.error = data.error;
            //                 self.tableData = data.data;
            //                 self.singleTestDraw();
            //             }
            //             else {
            //                 self.$message.error({
            //                     message: msg,
            //                     center: true,
            //                 })
            //             }
            //     })
            // },
            drawLine() {
                let myChart = echarts.init(document.getElementById('myChart'));
                // 绘制图表
                let option = {
                    title: {
                        text: '场景测试结果',
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#ccc'
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            crossStyle: {
                                color: '#999'
                            }
                        }
                    },
                    toolbox: {
                        feature: {
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    legend: {
                        data: ['成功次数', '失败次数', '成功率']
                    },
                    xAxis: [
                        {
                            type: 'category',
                            data: this.test_scenario,
                            axisPointer: {
                                type: 'shadow'
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '运行次数',
                            // min: 0,
                            // max: 100,
                            // interval: 20,
                            axisLabel: {
                                formatter: '{value} '
                            }
                        },
                    ],
                    series: [
                        {
                            name: '成功次数',
                            type: 'bar',
                            stack: '场景',
                            label: {
                                show: true,
                                position: 'insideRight'
                            },
                            data: this.successTimes
                            // data: [20, 10, 15, 2, 8, 56, 45, 10, 48, 1]
                        },
                        {
                            name: '失败次数',
                            type: 'bar',
                            stack: '场景',
                            label: {
                                show: true,
                                position: 'insideRight'
                            },
                            // yAxisIndex: 1,
                            data: this.failedTimes
                            // data: [1, 5, 7, 2, 5, 6, 1, 0, 4, 7]
                        },
                        {
                            name: '成功率',
                            type: 'line',
                            data: this.successRatio
                            // data: [79, 85, 78, 96, 87, 48, 54, 90, 52, 8]
                        },
                    ]
                };
                myChart.setOption(option);
            },

            drawFailLine() {
                let myChart = echarts.init(document.getElementById('myFailChart'));
                // 绘制图表
                let option = {
                    title: {
                        text: '失败接口统计',
                        left: 'center',
                        top: 20,
                        textStyle: {
                            color: '#ccc'
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    toolbox: {
                        feature: {
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    legend: {
                        data: ['失败次数']
                    },
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: this.fail_data_name,
                    },
                    series: [
                        {
                            name: '失败次数',
                            type: 'bar',
                            data: this.fail_data_count,
                            label: {
                                show: true,
                                position: 'insideRight'
                            },
                            // data: [20, 10, 15, 2, 8, 56, 45, 10, 48, 1]
                        },

                    ]
                };
                myChart.setOption(option);
            },
            singleTestDraw() {
                let myChart = echarts.init(document.getElementById('singleTestChart'));
                // 绘制图表
                let option = {
                    title: {
                        text: '比例图',
                        x: 'center'
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        type: 'scroll',
                        orient: 'vertical',
                        right: 10,
                        top: 20,
                        bottom: 20,
                    },
                    toolbox: {
                        feature: {
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    series: [
                        {
                            // name: '姓名',
                            type: 'pie',
                            radius: '50%',
                            center: ['50%', '50%'],
                            data: [
                                {value: this.error, name: 'ERROR'},
                                {value: this.fail, name: 'FAIL'},
                                {value: this.pass, name: 'PASS'},
                                // {value:'90', name:'ERROR'},
                                // {value:'5', name:'FAIL'},
                                // {value:'5', name:'PASS'},
                            ],
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                };
                myChart.setOption(option);
            },
            tableRowStyle(row) {
                if (row.result === 'ERROR' || row.result === 'FAIL') {
                    return "background-color: #DC143C;"
                } else if (row.result === 'TimeOut') {
                    return "background-color: #FFE4C4;"
                }
            },
            filterHandler(value, row, column) {
                return row.result === value;
            },
            // getTenTestTime(){
            //     let self = this;
            //     let params = {
            //         project_id: this.$route.params.project_id
            //     };
            //     let headers = {
            //         "Content-Type": "application/json",
            //         Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
            //     };
            //     getTestTenTime(headers, params).then(_data => {
            //         let {msg, code, data} = _data;
            //         if (code === '999999') {
            //             self.options = data;
            //             if (data.length) {
            //                 self.time = data[0].startTime;
            //                 self.elapsedTime = data[0].elapsedTime;
            //                 self.host = data[0].host;
            //                 self.getTestResult();
            //             }
            //         }
            //         else {
            //             self.$message.error({
            //                 message: msg,
            //                 center: true,
            //             })
            //         }
            //     })
            // },
            // changeHost(){
            //     for (let i=0;i<this.options.length;i++){
            //         if (this.options[i]['startTime'] === this.time){
            //             this.host = this.options[i].host;
            //             this.elapsedTime = this.options[i].elapsedTime;
            //         }
            //     }
            // },
            // getLatelyTenTestResult(){
            //     let self = this;
            //     let params = {
            //         project_id: this.$route.params.project_id
            //     };
            //     let headers = {
            //         "Content-Type": "application/json",
            //         Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
            //     };
            //     getTestTenResult(headers, params).then(_data => {
            //         let {msg, code, data} = _data;
            //         if (code === '999999') {
            //             console.log(data);
            //             data.forEach((item) => {
            //                 self.latelyTenPass.push(item.pass*100);
            //                 self.successTimes.push(item.fail*100);
            //                 self.latelyTenError.push(item.error*100)
            //             });
            //             self.drawLine()
            //         }
            //         else {
            //             self.$message.error({
            //                 message: msg,
            //                 center: true,
            //             })
            //         }
            //     })
            // }
        },
        watch: {
            // time(){
            //     this.getTestResult();
            //     this.changeHost()
            // },
            // timeArray(){
            //     console.log(this.timeArray)
            // }
        }
    }
</script>

<style scoped>
    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }

    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
</style>
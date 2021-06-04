<template>
    <section>
         <el-row class="toolbar" >
            <el-col :span="11" :inline="true">
                <div class="block" >
                    <span class="demonstration">开始和结束时间：</span>
                    <el-date-picker
                      v-model="timeArray"
                      type="daterange"
                      range-separator="至"
                      start-placeholder="开始日期"
                      end-placeholder="结束日期"
                      align="right">
                    </el-date-picker>
                </div>
            </el-col>
            <el-col :span="6" :inline="true">
                <el-button type="primary" @click="getGitLine" :loading="listLoading">查询</el-button>
            </el-col>
            <P style="color: red; margin: 0px">git工程较多，时间较慢，请耐心等待</P>
        </el-row>
        <el-row :gutter="24">
            <el-col :span="24">
                <div id="myChart" :style="{height: '1200px'}"></div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
    //import NProgress from 'nprogress'
    import echarts from 'echarts'
    import moment from "moment"
    import { getGitAllLine } from '../api/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                listLoading: false,
                timeArray: [],
                userSubmit: {},
                submitTotal: 0,
            }
        },
        methods: {
            drawLine(){
                let myChart = echarts.init(document.getElementById('myChart'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        text: '代码提交量汇总: 总量' + self.submitTotal + '行',
                        subtext: '数据来自gitlab'   ,
                        x:'center'
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
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: Object.keys(self.userSubmit),
                    },
                    series: [
                        {
                            name: '代码提交行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit),
                        }
                    ]
                };
                myChart.setOption(option);
            },
            getGitLine() {
                let self = this;
                this.listLoading = true;
                let params = {
                    startTime: moment(self.timeArray[0]).format("YYYY-MM-DD"),
                    endTime: moment(self.timeArray[1]).format("YYYY-MM-DD"),
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getGitAllLine(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.userSubmit = data.userSubmit;
                        self.submitTotal = data.submitTotal;
                        self.drawLine();
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
        }
    }

</script>

<style>

</style>
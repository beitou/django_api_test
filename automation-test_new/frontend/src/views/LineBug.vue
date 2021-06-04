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
                <el-button type="primary" @click="getLineBugs" :loading="listLoading">查询</el-button>
            </el-col>
<!--             <el-col :span="6" :inline="true">-->
<!--                 <el-button type="primary" @click="export" :loading="exportLoading">导出</el-button>-->
<!--             </el-col>-->
            <P style="color: red; margin: 0px">git工程较多，时间较慢，请耐心等待</P>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">H5</span></div>-->
        <el-row :gutter="5">
<!--                <div class="tableTitle"><span class="midText">H5</span></div><br>-->
                <el-col :span="8"><div id="myChart_h5_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_h5_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_h5_lv" :style="{height: '400px'}" ></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_h5_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_h5_rq" :style="{height: '400px'}"></div></el-col>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">商家&店铺</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_jiangxun_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_jiangxun_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_jiangxun_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_jiangxun_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_jiangxun_rq" :style="{height: '400px'}"></div></el-col>
<!--            style="word-wrap: break-word;"-->
        </el-row>
<!--        <div class="tableTitle"><span class="midText">APP</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_app_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_app_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_app_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_app_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_app_rq" :style="{height: '400px'}"></div></el-col>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">订单&财务</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_qiuyu_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_qiuyu_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_qiuyu_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_qiuyu_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_qiuyu_rq" :style="{height: '400px'}"></div></el-col>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">商品&搜索</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_baiju_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_baiju_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_baiju_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_baiju_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_baiju_rq" :style="{height: '400px'}"></div>
                </el-col>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">派单&履约</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_daxiong_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_daxiong_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_daxiong_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_daxiong_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_daxiong_rq" :style="{height: '400px'}"></div></el-col>
        </el-row>
<!--        <div class="tableTitle"><span class="midText">营销&导购</span></div>-->
        <el-row :gutter="5">
                <el-col :span="8"><div id="myChart_shenmu_hs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_shenmu_bs" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_shenmu_lv" :style="{height: '400px'}"></div></el-col>
        </el-row>
        <el-row :gutter="8">
                <el-col :span="8"><div id="myChart_shenmu_sc" :style="{height: '400px'}"></div></el-col>
                <el-col :span="8"><div id="myChart_shenmu_rq" :style="{height: '400px'}"></div></el-col>
        </el-row>
<!--        <el-row :gutter="24">-->
<!--            <el-col :span="24">-->
<!--                <div id="myChart_h5_bs" :style="{height: '300px'}"></div>-->
<!--            </el-col>-->
<!--        </el-row>-->
    </section>
</template>

<div id="app">
  <div class="static"
     v-bind:class="{ 'barWidth': barWidth }">
  </div>
</div>

<script>
    import echarts from 'echarts'
    import moment from "moment"
    import { getCodeQuality } from '../api/api';
    export default {
        data() {
            return {
                listLoading: false,
                timeArray: [],
                userSubmit: {},
                codeQualith:{},
                resolved_dict:{},
                solution_times:{},
                daily_clearance_rates:{}
            }
        },
        methods: {
            drawLine_h5_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_h5_hs = echarts.init(document.getElementById('myChart_h5_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    // formatter: function(params) {
                    //     var relVal = params[0].name;
                    //     var value = 0;
                    //     for (var i = 0, l = params.length; i < l; i++) {
                    //         value += params[i].value;
                    //     }
                    //     for (var i = 0, l = params.length; i < l; i++) {
                    //         relVal +=  '<br>' + params[i].seriesName + ' : ' + (100 * parseFloat(params[i].value) / parseFloat(value)).toFixed(2) + "%";
                    //     }
                    //     return relVal;
                    // },
                    title: {
                        left: '5%',
                        text: 'H5团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.h5)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.h5)
                        }
                    ]
                };
                myChart_h5_hs.setOption(option);
            },
            drawLine_h5_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_h5_bs = echarts.init(document.getElementById('myChart_h5_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'H5团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.h5)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.h5)
                        }
                    ]
                };
                myChart_h5_bs.setOption(option);
            },
            drawLine_h5_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_h5_lv = echarts.init(document.getElementById('myChart_h5_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'H5团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.h5)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.h5)
                        }
                    ]
                };
                myChart_h5_lv.setOption(option);
            },
            drawLine_h5_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_h5_sc = echarts.init(document.getElementById('myChart_h5_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'H5团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.h5)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.h5)
                        }
                    ]
                };
                myChart_h5_sc.setOption(option);
            },
            drawLine_h5_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_h5_rq = echarts.init(document.getElementById('myChart_h5_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    // formatter: function(params) {
                    //     var relVal = params[0].name;
                    //     var value = 0;
                    //     for (var i = 0, l = params.length; i < l; i++) {
                    //         value += params[i].value;
                    //     }
                    //     for (var i = 0, l = params.length; i < l; i++) {
                    //         relVal +=  '<br>' + params[i].seriesName + ' : ' + (100 * parseFloat(params[i].value) / parseFloat(value)).toFixed(2) + "%";
                    //     }
                    //     return relVal;
                    // },
                    title: {
                        left: '5%',
                        text: 'H5团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        // max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: Object.keys(self.daily_clearance_rates.h5)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.h5)
                        }
                    ]
                };
                myChart_h5_rq.setOption(option);
            },

            drawLine_app_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_app_hs = echarts.init(document.getElementById('myChart_app_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'app团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.app)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.app)
                        }
                    ]
                };
                myChart_app_hs.setOption(option);
            },
            drawLine_app_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_app_bs = echarts.init(document.getElementById('myChart_app_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'app团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.app)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.app)
                        }
                    ]
                };
                myChart_app_bs.setOption(option);
            },
            drawLine_app_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_app_lv = echarts.init(document.getElementById('myChart_app_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'app团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.app)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.app)
                        }
                    ]
                };
                myChart_app_lv.setOption(option);
            },
            drawLine_app_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_app_sc = echarts.init(document.getElementById('myChart_app_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'app团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.app)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.app)
                        }
                    ]
                };
                myChart_app_sc.setOption(option);
            },
            drawLine_app_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_app_rq = echarts.init(document.getElementById('myChart_app_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: 'app团队',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        // max: value.max(10),
                        data: Object.keys(self.daily_clearance_rates.app)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.app)
                        }
                    ]
                };
                myChart_app_rq.setOption(option);
            },

            drawLine_baiju_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_baiju_hs = echarts.init(document.getElementById('myChart_baiju_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商品&搜索',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.bai_ju)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.bai_ju)
                        }
                    ]
                };
                myChart_baiju_hs.setOption(option);
            },
            drawLine_baiju_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_baiju_bs = echarts.init(document.getElementById('myChart_baiju_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商品&搜索',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.bai_ju)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.bai_ju)
                        }
                    ]
                };
                myChart_baiju_bs.setOption(option);
            },
            drawLine_baiju_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_baiju_lv = echarts.init(document.getElementById('myChart_baiju_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商品&搜索',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.bai_ju)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.bai_ju)
                        }
                    ]
                };
                myChart_baiju_lv.setOption(option);
            },
            drawLine_baiju_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_baiju_sc = echarts.init(document.getElementById('myChart_baiju_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商品&搜索',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.bai_ju)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.bai_ju)
                        }
                    ]
                };
                myChart_baiju_sc.setOption(option);
            },
            drawLine_baiju_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_baiju_rq = echarts.init(document.getElementById('myChart_baiju_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商品&搜索',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: Object.keys(self.daily_clearance_rates.bai_ju)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.bai_ju)
                        }
                    ]
                };
                myChart_baiju_rq.setOption(option);
            },

            drawLine_qiuyu_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_qiuyu_hs = echarts.init(document.getElementById('myChart_qiuyu_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '订单&财务',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.qiu_yu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.qiu_yu)
                        }
                    ]
                };
                myChart_qiuyu_hs.setOption(option);
            },
            drawLine_qiuyu_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_qiuyu_bs = echarts.init(document.getElementById('myChart_qiuyu_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '订单&财务',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.qiu_yu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.qiu_yu)
                        }
                    ]
                };
                myChart_qiuyu_bs.setOption(option);
            },
            drawLine_qiuyu_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_qiuyu_lv = echarts.init(document.getElementById('myChart_qiuyu_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '订单&财务',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.qiu_yu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.qiu_yu)
                        }
                    ]
                };
                myChart_qiuyu_lv.setOption(option);
            },
            drawLine_qiuyu_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_qiuyu_sc = echarts.init(document.getElementById('myChart_qiuyu_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '订单&财务',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.qiu_yu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.qiu_yu)
                        }
                    ]
                };
                myChart_qiuyu_sc.setOption(option);
            },
            drawLine_qiuyu_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_qiuyu_rq = echarts.init(document.getElementById('myChart_qiuyu_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '订单&财务',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: Object.keys(self.daily_clearance_rates.qiu_yu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.qiu_yu)
                        }
                    ]
                };
                myChart_qiuyu_rq.setOption(option);
            },

            drawLine_jiangxun_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_jiangxun_hs = echarts.init(document.getElementById('myChart_jiangxun_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商家&店铺',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.jiang_xun)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.jiang_xun)
                        }
                    ]
                };
                myChart_jiangxun_hs.setOption(option);
            },
            drawLine_jiangxun_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_jiangxun_bs = echarts.init(document.getElementById('myChart_jiangxun_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商家&店铺',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.jiang_xun)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.jiang_xun)
                        }
                    ]
                };
                myChart_jiangxun_bs.setOption(option);
            },
            drawLine_jiangxun_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_jiangxun_lv = echarts.init(document.getElementById('myChart_jiangxun_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商家&店铺',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.jiang_xun)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.jiang_xun)
                        }
                    ]
                };
                myChart_jiangxun_lv.setOption(option);
            },
            drawLine_jiangxun_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_jiangxun_sc = echarts.init(document.getElementById('myChart_jiangxun_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商家&店铺',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.jiang_xun)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.jiang_xun)
                        }
                    ]
                };
                myChart_jiangxun_sc.setOption(option);
            },
            drawLine_jiangxun_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_jiangxun_rq = echarts.init(document.getElementById('myChart_jiangxun_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '商家&店铺',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        data: Object.keys(self.daily_clearance_rates.jiang_xun)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.jiang_xun)
                        }
                    ]
                };
                myChart_jiangxun_rq.setOption(option);
            },

            drawLine_daxiong_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_daxiong_hs = echarts.init(document.getElementById('myChart_daxiong_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '派单&履约',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.da_xiong)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.da_xiong)
                        }
                    ]
                };
                myChart_daxiong_hs.setOption(option);
            },
            drawLine_daxiong_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_daxiong_bs = echarts.init(document.getElementById('myChart_daxiong_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '派单&履约',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.da_xiong)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.da_xiong)
                        }
                    ]
                };
                myChart_daxiong_bs.setOption(option);
            },
            drawLine_daxiong_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_daxiong_lv = echarts.init(document.getElementById('myChart_daxiong_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '派单&履约',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.da_xiong)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.da_xiong)
                        }
                    ]
                };
                myChart_daxiong_lv.setOption(option);
            },
            drawLine_daxiong_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_daxiong_sc = echarts.init(document.getElementById('myChart_daxiong_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '派单&履约',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.da_xiong)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.da_xiong)
                        }
                    ]
                };
                myChart_daxiong_sc.setOption(option);
            },
            drawLine_daxiong_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_daxiong_rq = echarts.init(document.getElementById('myChart_daxiong_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '派单&履约',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        min: '5',
                        data: Object.keys(self.daily_clearance_rates.da_xiong)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.da_xiong)
                        }
                    ]
                };
                myChart_daxiong_rq.setOption(option);
            },

            drawLine_shenmu_hs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_shenmu_hs = echarts.init(document.getElementById('myChart_shenmu_hs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '营销&导购',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['代码行数']
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
                        right: '3%',
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
                        data: Object.keys(self.userSubmit.shen_mu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '代码行数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.userSubmit.shen_mu)
                        }
                    ]
                };
                myChart_shenmu_hs.setOption(option);
            },
            drawLine_shenmu_bs() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_shenmu_bs = echarts.init(document.getElementById('myChart_shenmu_bs'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '营销&导购',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug数']
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
                        right: '3%',
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
                        data: Object.keys(self.resolved_dict.shen_mu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict.shen_mu)
                        }
                    ]
                };
                myChart_shenmu_bs.setOption(option);
            },
            drawLine_shenmu_lv() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_shenmu_lv = echarts.init(document.getElementById('myChart_shenmu_lv'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '营销&导购',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['千行代码bug率']
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
                        right: '3%',
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
                        data: Object.keys(self.codeQualith.shen_mu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: '千行代码bug率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.codeQualith.shen_mu)
                        }
                    ]
                };
                myChart_shenmu_lv.setOption(option);
            },
            drawLine_shenmu_sc() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_shenmu_sc = echarts.init(document.getElementById('myChart_shenmu_sc'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '营销&导购',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug平均解决时长/h']
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
                        right: '3%',
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
                        data: Object.keys(self.solution_times.shen_mu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug平均解决时长/h',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.solution_times.shen_mu)
                        }
                    ]
                };
                myChart_shenmu_sc.setOption(option);
            },
            drawLine_shenmu_rq() {
                // var data = new Array();
                // data.push(Object.keys(self.h5));
                let myChart_shenmu_rq = echarts.init(document.getElementById('myChart_shenmu_rq'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        left: '5%',
                        text: '营销&导购',
                        subtext: '数据来自禅道'
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    legend: {
                        left: '30%',
                        data: ['bug日清率']
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
                        right: '3%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value',
                        min: 0,
                        max: 100,
                        //max: self.bugTotal,
                        boundaryGap: [0, 0.01]
                    },
                    yAxis: {
                        type: 'category',
                        min: '5',
                        data: Object.keys(self.daily_clearance_rates.shen_mu)
                    },
                    series: [
                        {
                            barMaxWidth: '35%',
                            name: 'bug日清率',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.daily_clearance_rates.shen_mu)
                        }
                    ]
                };
                myChart_shenmu_rq.setOption(option);
            },

            getLineBugs(){
                let self = this;
                this.listLoading = true;
                let params = {
                    startTime: moment(self.timeArray[0]).format("YYYY-MM-DD"),
                    endTime: moment(self.timeArray[1]).format("YYYY-MM-DD"),
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getCodeQuality(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        //代码行数
                        self.userSubmit = data.userSubmit;
                        //bug率
                        self.codeQualith = data.codeQualith;
                        //bug数
                        self.resolved_dict = data.resolved_dict;
                        //平均解决时间
                        self.solution_times = data.solution_times;
                        //日清率
                        self.daily_clearance_rates = data.daily_clearance_rates;
                        /*
                        3.页面格子展示
                        2.计算平均值
                        1.前端代码优化
                        drawline(team_name):
                            self.drawLine_bug率(team_name);
                            self.drawLine_代码数(team_name);
                            '代码行数', 'bug数', '千行代码bug率', 'bug平均解决时长/h', 'bug日清率'
                        for team_name in team:
                            self.drawLine(team_name);
                        */
                        self.drawLine_h5_hs();
                        self.drawLine_h5_bs();
                        self.drawLine_h5_lv();
                        self.drawLine_h5_sc();
                        self.drawLine_h5_rq();
                        self.drawLine_app_hs();
                        self.drawLine_app_bs();
                        self.drawLine_app_lv();
                        self.drawLine_app_sc();
                        self.drawLine_app_rq();
                        self.drawLine_baiju_hs();
                        self.drawLine_baiju_bs();
                        self.drawLine_baiju_lv();
                        self.drawLine_baiju_sc();
                        self.drawLine_baiju_rq();
                        self.drawLine_qiuyu_hs();
                        self.drawLine_qiuyu_bs();
                        self.drawLine_qiuyu_lv();
                        self.drawLine_qiuyu_sc();
                        self.drawLine_qiuyu_rq();
                        self.drawLine_jiangxun_hs();
                        self.drawLine_jiangxun_bs();
                        self.drawLine_jiangxun_lv();
                        self.drawLine_jiangxun_sc();
                        self.drawLine_jiangxun_rq();
                        self.drawLine_daxiong_hs();
                        self.drawLine_daxiong_bs();
                        self.drawLine_daxiong_lv();
                        self.drawLine_daxiong_sc();
                        self.drawLine_daxiong_rq();
                        self.drawLine_shenmu_hs();
                        self.drawLine_shenmu_bs();
                        self.drawLine_shenmu_lv();
                        self.drawLine_shenmu_sc();
                        self.drawLine_shenmu_rq();
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            }
            // ,
            // export(){
            //     let self = this;
            //     this.listLoading = true;
            //     let params = {
            //         startTime: moment(self.timeArray[0]).format("YYYY-MM-DD"),
            //         endTime: moment(self.timeArray[1]).format("YYYY-MM-DD"),
            //     };
            //     let headers = {
            //         Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
            //     };
            // }
        },
        mounted() {
        }
    }
</script>

<style lang="scss" scoped>
    .tableTitle {
        position: relative;
        margin: 0 auto;
        width: 600px;
        height: 1px;
        background-color: #d4d4d4;
        text-align: center;
        font-size: 16px;
        color: rgba(101, 101, 101, 1);
      }
     .midText {
        position: absolute;
        left: 50%;
        background-color: #ffffff;
        padding: 0 15px;
        transform: translateX(-50%) translateY(-50%);
      }
</style>
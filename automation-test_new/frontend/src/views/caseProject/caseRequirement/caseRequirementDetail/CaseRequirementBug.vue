<template>
    <div class="main">
        <el-row :gutter="24">
            <el-col :span="22">
                <div id="myChart" :style="{height: '500px'}"></div>
            </el-col>
        </el-row>
        <el-row :span="24">
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{bugTotal}}个</h1>
                    <div>总BUG数</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{closedCount}}个</h1>
                    <div>已关闭BUG数</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{closed_rate}}</h1>
                    <div>BUG关闭率</div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :span="24">
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{p1Count}}个</h1>
                    <div>P1BUG数</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{p2Count}}个</h1>
                    <div>P2BUG数</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{p3Count}}个</h1>
                    <div>P3BUG数</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h1>{{p4Count}}个</h1>
                    <div>P4BUG数</div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import echarts from 'echarts'
    import { getZentaoBug } from '../../../../api/api'
    export default {
        data() {
            return {
                bugTotal: 0,
                closedCount: 0,
                closed_rate: '0.00%',
                p1Count: 0,
                p2Count: 0,
                p3Count: 0,
                p4Count: 0,
                resolved_dict: {},
            }
        },
        methods: {
            drawLine(){
                let myChart = echarts.init(document.getElementById('myChart'));
                // 绘制图表
                let self = this;
                let option = {
                    title: {
                        text: '已关闭BUG人员分布',
                        subtext: '数据来自蝉道'   ,
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
                        data: Object.keys(self.resolved_dict),
                    },
                    series: [
                        {
                            name: 'bug数',
                            type: 'bar',
                            label: {
                                normal: {
                                    position: 'right',
                                    show: true
                                }
                            },
                            data: Object.values(self.resolved_dict),
                        }
                    ]
                };
                myChart.setOption(option);
            },
            getBug() {
                this.listLoading = true;
                let self = this;
                let params = {
                    zentao_id: this.$route.params.zenTao_id,
                };
                let headers = {
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getZentaoBug(headers, params).then(_data => {
                    let { msg, code, data } = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.bugTotal = data.total;
                        self.closedCount = data.closed;
                        self.p1Count = data.p1;
                        self.p2Count = data.p2;
                        self.p3Count = data.p3;
                        self.p4Count = data.p4;
                        self.resolved_dict = data.resolved_dict;
                        self.closed_rate = data.closed_rate + '%';
                        self.drawLine();
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
        },
        mounted() {
            this.getBug();
        }
    }
</script>

<style lang="scss" scoped>
    .box-card {
        width: 100%;
        height: 100%;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .member {
        width: 7%;
    }
    .main {
        margin: 35px;
        margin-top: 10px;
    }
    .inline {
        margin: 10px;
        margin-left: 0px;
        margin-right: 20px;
    }
</style>


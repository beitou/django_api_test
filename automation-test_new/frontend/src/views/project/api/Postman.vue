<template>
    <section>
        <router-link :to="{ name: '新增接口', params: {project_id: this.$route.params.project_id, formData: this.form, _type: this.radio, _typeData: this.radioType}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list">快速新建API</el-button>
        </router-link>
        <el-form :model="form" ref="form" :rules="formRules">
            <el-col :span="3" class="HOST">
                <el-form-item prop="url">
                    <el-select v-model="form.url"  placeholder="测试环境">
                        <el-option v-for="(item,index) in Host" :key="index+''" :label="item.name" :value="item.host"></el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;padding-bottom: 0px">
                <el-row :gutter="10">  <!--gutter ,间隔 -->
                    <el-col :span="3">
                        <el-form-item>
                            <el-select v-model="form.request4" placeholder="请求方式" @change="checkRequest">
                                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="3">
                        <el-form-item>
                            <el-select v-model="form.Http4" placeholder="HTTP协议">
                                <el-option v-for="(item,index) in Http" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span='16'>
                        <el-form-item prop="addr">
                            <el-input v-model.trim="form.addr" placeholder="地址" auto-complete @change="analysisAddr"></el-input>
                        </el-form-item>
                    </el-col>

                    <el-col :span='2'>
                        <el-button type="primary" @click="fastTest">发送</el-button>
                    </el-col>
                </el-row>
            </div>
            <el-row :span="24" v-show="postData" >
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="textarea"
                @change="analysiPostData">
                </el-input>
            </el-row>
            <el-row :span="24">
                <el-collapse v-model="activeNames" @change="handleChange">
                    <el-collapse-item title="请求头部" name="1">
                        <el-row :span="24" v-show="true" >
                <el-input
                  type="textarea"
                  :rows="2"
                  placeholder="请输入内容"
                  v-model="textarea"
                @change="analysiHeadData">
                </el-input>
            </el-row>
                        <el-table :data="form.head" highlight-current-row ref="multipleHeadTable">
                            <el-table-column type="selection" min-width="5%" label="头部">
                            </el-table-column>
                            <el-table-column prop="name" label="标签" min-width="20%" sortable>
                                <template slot-scope="scope">
                                    <el-select placeholder="head标签" filterable v-model="scope.row.name">
                                        <el-option v-for="(item,index) in header" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                    <el-input class="selectInput" v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="内容" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="7%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delHead(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(form.head.length-1)" size="mini" class="el-icon-plus" @click="addHead"></el-button>
                                </template>
                            </el-table-column>
                            <el-table-column min-width="18%">

                            </el-table-column>
                        </el-table>
                    </el-collapse-item>
                    <el-collapse-item title="请求参数" name="2">
                        <div style="margin: 5px">
                            <el-row :span="24">
                                <el-col :span="4"><el-radio v-model="radio" label="form-data">表单(form-data)</el-radio></el-col>
                                <el-col :span="4"><el-radio v-model="radio" label="raw" v-if="request3">源数据(raw)</el-radio></el-col>
                                <el-col v-show="request3" :span="16"><el-checkbox v-model="radioType" label="3" v-show="ParameterTyep">表单转源数据</el-checkbox></el-col>
                            </el-row>
                        </div>
                        <el-table ref="multipleParameterTable" :data="form.parameter" highlight-current-row :class="ParameterTyep? 'parameter-a': 'parameter-b'" @selection-change="selsChangeParameter">
                            <el-table-column type="selection" min-width="5%" label="头部">
                            </el-table-column>
                            <el-table-column prop="name" label="参数名" min-width="20%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="参数值" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="7%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delParameter(scope.$index)"></i>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="10%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(form.parameter.length-1)" size="mini" class="el-icon-plus" @click="addParameter"></el-button>
                                </template>
                            </el-table-column>
                            <el-table-column label="" min-width="18%"></el-table-column>
                        </el-table>
                        <template>
                            <el-input :class="ParameterTyep? 'parameter-b': 'parameter-a'" type="textarea" :rows="5" placeholder="请输入内容" v-model.trim="form.parameterRaw"></el-input>
                        </template>
                    </el-collapse-item>
                    <el-collapse-item title="响应结果" name="4">
                        <div style="margin-bottom: 10px">
                            <el-button @click="showBody">Body</el-button>
                            <el-button @click="showHeader">Head</el-button>
                            <!--<el-button type="primary" @click="neatenFormat">格式转换</el-button>-->
                        </div>
                        <el-card class="box-card">
                            <div slot="header" class="clearfix">
                                <span v-model="form.statusCode" style="font-size: 25px">{{form.statusCode}}</span>
                            </div>
                            <div v-model="form.resultData" :class="resultShow? 'parameter-a': 'parameter-b'" v-show="form.resultData&&resultShow">
                                <div style="word-break: break-all;overflow:auto;overflow-x:hidden">
                                    {{form.resultData}}
                                </div>
                                <pre id ='resultData' style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden" @click="neatenFormat('resultData')">{{form.resultData}}
                                </pre>
                            </div>

                            <div v-show="!resultShow">
                                <div v-model="form.resultHead">{{form.resultHead}}</div>
                                <pre id ='resultHead' style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden" @click="neatenFormat('resultHead')">{{form.resultHead}}
                                </pre>
                            </div>
                            <div v-show="!form.resultData&&!form.resultHead" class="raw">暂无数据</div>
                        </el-card>
                    </el-collapse-item>
                </el-collapse>
            </el-row>
        </el-form>
    </section>
</template>
<script>
    import $ from 'jquery'
    import VuePopper from "element-ui/src/utils/vue-popper";
    import { test,requrl,requrl_post,getHost} from '../../../api/api'

    export default {
        components: {VuePopper},
        data() {
            return {
                request: [{value: 'get', label: 'GET'},
                    {value: 'post', label: 'POST'},
                    {value: 'put', label: 'PUT'},
                    {value: 'delete', label: 'DELETE'}],
                Http: [{value: 'http', label: 'HTTP'},
                    {value: 'https', label: 'HTTPS'}],
                ParameterTyep: true,
                radio: "form-data",
                loadingSend: false,
                header: [{value: 'Accept', label: 'Accept'},
                    {value: 'Accept-Charset', label: 'Accept-Charset'},
                    {value: 'Accept-Encoding', label: 'Accept-Encoding'},
                    {value: 'Accept-Language', label: 'Accept-Language'},
                    {value: 'Accept-Ranges', label: 'Accept-Ranges'},
                    {value: 'Authorization', label: 'Authorization'},
                    {value: 'Cache-Control', label: 'Cache-Control'},
                    {value: 'Connection', label: 'Connection'},
                    {value: 'Cookie', label: 'Cookie'},
                    {value: 'Content-Length', label: 'Content-Length'},
                    {value: 'Content-Type', label: 'Content-Type'},
                    {value: 'Content-MD5', label: 'Content-MD5'},
                    {value: 'Date', label: 'Date'},
                    {value: 'Expect', label: 'Expect'},
                    {value: 'From', label: 'From'},
                    {value: 'Host', label: 'Host'},
                    {value: 'If-Match', label: 'If-Match'},
                    {value: 'If-Modified-Since', label: 'If-Modified-Since'},
                    {value: 'If-None-Match', label: 'If-None-Match'},
                    {value: 'If-Range', label: 'If-Range'},
                    {value: 'If-Unmodified-Since', label: 'If-Unmodified-Since'},
                    {value: 'Max-Forwards', label: 'Max-Forwards'},
                    {value: 'Origin', label: 'Origin'},
                    {value: 'Pragma', label: 'Pragma'},
                    {value: 'Proxy-Authorization', label: 'Proxy-Authorization'},
                    {value: 'Range', label: 'Range'},
                    {value: 'Referer', label: 'Referer'},
                    {value: 'TE', label: 'TE'},
                    {value: 'Upgrade', label: 'Upgrade'},
                    {value: 'User-Agent', label: 'User-Agent'},
                    {value: 'Via', label: 'Via'},
                    {value: 'Warning', label: 'Warning'},
                    {value: 'Access-Control-Allow-Origin', label: 'Access-Control-Allow-Origin'}],
                header4: "",
                radioType: "",
                result: true,
                activeNames: ['1', '2', '3', '4'],
                Host: [{name: "", host: ""}],
                id: "",
                request3: true,
                form: {
                    url:"",
                    request4: 'GET',
                    Http4: 'HTTP',
                    addr: '',
                    head: [
                        {name: "", value: ""},
                        ],
                    parameterRaw: "",
                    parameter: [{name: "", value: "", required:"", restrict: "", description: ""},

                    ],
                    parameterType: "",
                    statusCode: "",
                    resultData: "",
                    resultHead: "",
                },
                formRules: {
                    addr: [
                        { required: true, message: '请输入地址', trigger: 'blur' },
                    ]
                },
                headers: "",
                parameters: "",
                resultShow: true,
                format: false,
                postData:false,
            }
        },
        methods: {
            checkRequest(){
                console.log(this.form.request4);
                let request = this.form.request4;
                if (request==="GET" || request==="DELETE"){
                    this.request3=false
                } else {
                    this.request3=true
                }
                if (request==="post"){
                    this.postData=true
                }else{
                    this.postData=false
                }
            },
            isJsonString(str) {
                try {
                    if (typeof JSON.parse(str) === "object") {
                        return true;
                    }
                } catch(e) {
                }
                return false;
            },

            getHost() {
                let self = this;
                let params = {
                                project_id: Number(this.$route.params.project_id),
                                page: this.page,
                            };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                getHost(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    console.log(msg,code,data);
                    if (code === '999999') {
                        data.data.forEach((item) => {
                            if (item.status) {
                                self.Host.push(item)
                            }
                        })
                    }

                });

            },

            fastTest: function() {

                let host = this.form.addr;
                if (host.indexOf("http://") ===0){
                    this.form.addr = host.slice(7).split("?")[0];
                }
                if (host.indexOf("https://") ===0){
                    this.form.addr = host.slice(8).split("?")[0];
                }
                console.log(this.form.addr);
                this.$refs.form.validate((valid) => {
                    let that = this.$router;
                    if (valid) {
                        this.loadingSend = true;
                        let self = this;
                        let _parameter = new Object();
                        let headers = new Object();
                        let request_parameter_type;
                        self.form.statusCode = '';
                        self.form.resultData = '';
                        self.form.resultHead = '';
                        for (let i = 0; i < self.form.head.length; i++) {
                            var a = self.form.head[i]["name"];
                            if (a) {
                                headers[a] = self.form.head[i]["value"]
                            }
                        }
                        let url = self.form.Http4 + "://" + this.form.addr;
                        let _type = self.radio;
                        if (_type === 'form-data') {
                            for (let i = 0; i < self.parameters.length; i++) {
                                    var a = self.parameters[i]["name"];
                                    if (a) {
                                        _parameter[a] = self.parameters[i]["value"];
                                    }
                                }
                            if (self.radioType) {

                                _parameter = JSON.stringify(_parameter);
                                request_parameter_type='raw';
                            } else {
                                // _parameter = self.form.parameter;
                                request_parameter_type='form-data';
                            }
                        } else {
                            // POST(url, self.form.parameterRaw, headers)
                            _parameter = self.form.parameterRaw;
                            request_parameter_type='raw';
                        }
                        if (self.form.parameterRaw && _type === "raw") {
                            if (!self.isJsonString(self.form.parameterRaw)) {
                                self.$message({
                                    message: '源数据格式错误',
                                    center: true,
                                    type: 'error'
                                })
                            }
                        }
                        this.getRequestResult(headers,_parameter,request_parameter_type);
                    }
                });
                // this.format=true;
                // alert(this.form.resultData);
                // this.neatenFormat();
            },
            getRequestResult(header,parameter,request_parameter_type){
                if (this.form.request4.toLowerCase()==="get"){
                    this.requestUrl(header,parameter,request_parameter_type);
                } else if(this.form.request4.toLowerCase()==="post"){
                    this.requestUrl_post(header,parameter,request_parameter_type);
                }
            },
            requestUrl(header,parameter,request_parameter_type){
                let self = this;
                // parameter['data']=parameter;
                if (request_parameter_type==='raw'){
                    parameter = JSON.parse(parameter);
                }

                let params = parameter;
                parameter['request_parameter_type'] = request_parameter_type;
                parameter['url']=self.form.Http4 + "://" + this.form.addr;

                let headers=header;
                headers['Content-Type']='application/json';
                headers['Authorization']='Token '+JSON.parse(sessionStorage.getItem('token'));

                requrl(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    this.form.resultData=data['data'];
                    this.form.statusCode=code;
                    this.form.resultHead=data['Header'];
                })
            },
            requestUrl_post(header,parameter,request_parameter_type){
                let self = this;
                // parameter['data']=parameter;

                if (request_parameter_type==='raw'){
                    parameter = JSON.parse(parameter);
                }
                let params = parameter;
                parameter['request_parameter_type'] = request_parameter_type;
                parameter['url']=self.form.Http4 + "://" + this.form.addr;


                let headers=header;
                headers['Content-Type']='application/json';
                headers['Authorization']='Token '+JSON.parse(sessionStorage.getItem('token'));

                requrl_post(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    this.form.resultData=data['data'];
                    this.form.statusCode=code;
                    this.form.resultHead=data['Header'];
                })
            },
            neatenFormat(val) {
                console.log(val);
                let demo = document.getElementById(val);
                // alert(this.form.resultData);
                // demo.innerText=this.form.resultData;
                hljs.highlightBlock(demo);
                // this.format = !this.format
            },
            addHead() {
                let headers = {name: "", value: ""};
                this.form.head.push(headers);
                let rows = [this.form.head[this.form.head.length-1]];
                this.toggleHeadSelection(rows)
            },
            delHead(index) {
                if (this.form.head.length !== 1) {
                    this.form.head.splice(index, 1)
                }
            },
            addParameter() {
                let headers = {name: "", value: "", required:"True", restrict: "", description: ""};
                this.form.parameter.push(headers);
                let rows = [this.form.parameter[this.form.parameter.length-1]];
                this.toggleParameterSelection(rows)
            },
            delParameter(index) {
                if (this.form.parameter.length !== 1) {
                    this.form.parameter.splice(index, 1)
                }
            },
            addResponse() {
                let headers = {name: "", value: "", required:"True", restrict: "", description: ""};
                this.form.response.push(headers)
            },
            delResponse(index) {
                if (this.form.response.length !== 1) {
                    this.form.response.splice(index, 1)
                }
            },
            changeParameterType() {
                if (this.radio === 'form-data') {
                    this.ParameterTyep = !this.ParameterTyep
                } else {
                    this.ParameterTyep = !this.ParameterTyep
                }
            },
            showBody() {
                this.resultShow = true
            },
            showHeader() {
                this.resultShow = false
            },

            handleChange(val) {
            },
            onSubmit() {
                console.log('submit!');
            },
            //解析URL，把url内的参数
            analysisAddr(val){
                var temp = val+"";
                if (temp.indexOf("?")>0) {
                    let a = val.split("?")[1].split("&");
                    // this.
                    // this.form.parameter=[];
                    // this.toggleParameterSelection(this.form.parameter);
                    a.forEach(
                        a => {
                            let headers = {name: a.split("=")[0], value: a.split("=")[1], required: "True", restrict: "", description: ""};
                            this.form.parameter.push(headers);
                            // this.$refs.multipleParameterTable.toggleRowSelection(headers,true);
                            // this.toggleParameterSelection(this.form.parameter);
                        }
                    );

                }
                this.toggleParameterSelection(this.form.parameter);

            },
            analysiPostData(val){
                let a = val.split("\n");
                this.form.parameter=[];
                a.forEach(
                    a=>{
                        let parameter={name: a.split(":")[0].trim(), value: a.split(":")[1].trim(), required: "True", restrict: "True", description: ""};
                        this.form.parameter.push(parameter);
                    }
                );
                this.toggleParameterSelection(this.form.parameter);
            },
            analysiHeadData(val){
                let a = val.split("\n");
                // this.form.head=[];
                a.forEach(
                    a=>{
                        let header={name: a.split(":")[0].trim(), value: a.replace(a.split(":")[0]+":","")};
                        this.form.head.push(header);
                        // let rows = [this.form.head[this.form.head.length-1]];
                        // this.toggleParameterSelection(rows)
                    }
                );
                this.toggleHeadSelection(this.form.head);
            },
            toggleHeadSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleHeadTable.toggleRowSelection(row, true);
                });
            },

            toggleParameterSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleParameterTable.toggleRowSelection(row,true);
                });
            },
            selsChangeHead: function (sels) {
                this.headers = sels
            },
            selsChangeParameter: function (sels) {
                this.parameters = sels
            },
        },
        watch: {
            radio() {
                this.changeParameterType()
            }
        },
        mounted() {
            this.toggleHeadSelection(this.form.head);
            this.toggleParameterSelection(this.form.parameter);
            this.getHost()
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
        /*position:absolute;*/
        /*margin-left:7px;*/
        /*padding-left:10px;*/
        /*width: 63%;*/
        /*height:25px;*/
        /*left:1px;*/
        /*top:1px;*/
        /*border-bottom:0px;*/
        /*border-right:0px;*/
        /*border-left:0px;*/
        /*border-top:0px;*/
        position: absolute;
        /*margin-left: 7px;*/
        padding-left: 9px;
        width: 180px;
        /*border-radius:0px;*/
        /*height: 38px;*/
        left: 1px;
        border-right: 0px;
    }
    .raw {
        border: 1px solid #e6e6e6;
        margin-bottom: 10px;
        padding:15px;
        text-align: center
    }
    .HOST {
        position: absolute;
        right: 10px;
        top: 0px;
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

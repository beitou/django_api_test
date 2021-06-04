<template>
    <section>

        <!--<label>
            <textarea ref="mycode" class="codePython" v-model="code" style="height:200px;width:600px;"></textarea>
        </label>-->
        <codemirror v-model="code" :options="cmOptions"></codemirror>
        <label>
            <textarea class="codePython" v-model="resultCode" style="height:200px;width:700px;"></textarea>
        </label>

        <div>
            <el-button type="primary" @click.native="codeSubmit">提交</el-button>
        </div>

    </section>

</template>

<script>
    import "codemirror/theme/ambiance.css";
    import "codemirror/lib/codemirror.css";
    import "codemirror/addon/hint/show-hint.css";
    import { runCode } from '../../../../api/api';

    import { codemirror } from 'vue-codemirror'
    require("codemirror/mode/python/python.js");
    require('codemirror/addon/fold/foldcode.js');
    require('codemirror/addon/fold/foldgutter.js');
    require('codemirror/addon/fold/brace-fold.js');
    require('codemirror/addon/fold/xml-fold.js');
    require('codemirror/addon/fold/indent-fold.js');
    require('codemirror/addon/fold/markdown-fold.js');
    require('codemirror/addon/fold/comment-fold.js');


    export default {
        components:{
            codemirror
        },
        data () {
            return {
                code: '# 请输入代码',
                resultCode: '测试结果',
                cmOptions: {
                    // codemirror options
                    indentWithTabs: true,
                    smartIndent: true,
                    lineNumbers: true,
                    matchBrackets: true,
                    mode: 'python',
                    extraKeys: {'Command': 'autocomplete'},//自定义快捷键

                },
            }
        },
        mounted () {
            let mime = 'text';
            //let theme = 'ambiance'//设置主题，不设置的会使用默认主题
            /*let editor = CodeMirror.fromTextArea(this.$refs.mycode, {
                mode: mime,//选择对应代码编辑器的语言，我这边选的是数据库，根据个人情况自行设置即可
                indentWithTabs: true,
                smartIndent: true,
                lineNumbers: true,
                matchBrackets: true,
                //theme: theme,
                // autofocus: true,
                extraKeys: {'Command': 'autocomplete'},//自定义快捷键
                hintOptions: {//自定义提示选项
                tables: {
                    users: ['name', 'score', 'birthDate'],
                    countries: ['name', 'population', 'size']
                    }
                }
            });
        //代码自动提示功能，记住使用cursorActivity事件不要使用change事件，这是一个坑，那样页面直接会卡死
            let self = this;
            editor.on('cursorActivity', function () {
                editor.showHint();
                self.code = editor.getValue();
            });*/
        },
        methods: {
            codeSubmit: function () {
                let self = this;
                let params = {
                    code: self.code,
                };
                let headers = {
                    Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                };
                runCode(headers, params).then(_data => {
                    let {msg, code, data} = _data;
                    self.listLoading = false;
                    if (code === '999999') {
                        /*self.total = data.total;
                        self.caseList = data.data;*/
                        self.resultCode = data.resultCode;
                    } else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
        }
    }
</script>

<style>
  .codePython {
    font-size: 11pt;
    font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace, serif;
  }
</style>
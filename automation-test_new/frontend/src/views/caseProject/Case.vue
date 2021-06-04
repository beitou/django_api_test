<template>
    <section>
        <el-row :span="24" class="row-title">
            <el-col :span="24">
            </el-col>
            <!--新增-->
 <!--           <el-dialog title="新增分组" :visible.sync="addGroupFormVisible" :close-on-click-modal="false"
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
            &lt;!&ndash;编辑父分组&ndash;&gt;
            <el-dialog title="编辑分组" :visible.sync="editFirstGroupFormVisible" :close-on-click-modal="false"
                       style="width: 60%; left: 20%">
                <el-form :model="editFirstGroupForm" label-width="80px" :rules="editFirstGroupFormRules"
                         ref="editFirstGroupForm">
                    <el-form-item label="分组名称" prop='secondFirstGroup'>
                        <el-input v-model.trim="editFirstGroupForm.secondFirstGroup" auto-complete="off"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="editFirstGroupFormVisible = false">取消</el-button>
                    <el-button type="primary" @click.native="editFirstGroupSubmit" :loading="editFirstGroupLoading">提交
                    </el-button>
                </div>
            </el-dialog>-->
            <el-col :span="24">
                <div style="margin-left: 10px;margin-right: 20px">
                    <router-view></router-view>
                </div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
    import {addApiGroup, delApiGroup, getApiGroupList, updateApiGroup} from '../../api/api'

    export default {
        data() {
            return {
                caseProject: "",
                groupData: [],
                addGroupFormVisible: false,
                addGroupLoading: false,
                addFormVisible: false,//新增界面是否显示
                addGroupFormRules: {
                    firstgroup: [
                        {required: true, message: '请输入子分组名称', trigger: 'blur'},
                        // { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    ]
                },
                //新增界面数据
                addGroupForm: {
                    firstgroup: '',
                },
                editFirstGroupFormVisible: false,
                editFirstGroupLoading: false,
                editFirstFormVisible: false,//编辑界面是否显示
                editFirstGroupFormRules: {
                    secondFirstGroup: [
                        {required: true, message: '请输入分组名称', trigger: 'blur'},
                        // { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editFirstGroupForm: {
                    firstgroup: '',
                    second_id: '',
                },
                filters: {
                    name: ''
                },
                api: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                apiView: true,
            }
        },
        methods: {
            // 初始化
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            }
        },
        mounted() {
        }
    }

</script>

<style lang="scss" scoped>
    .api-title {
        padding: 15px;
        margin: 0px;
        text-align: center;
        border-radius: 5px;
        font-size: 15px;
        color: aliceblue;
        background-color: rgb(32, 160, 255);
        //background-color: rgb(58, 58, 58);
        font-family: PingFang SC;
    }

    .api-title1 {
        padding: 15px;
        margin: 0px;
        text-align: center;
        border-radius: 5px;
        font-size: 15px;
        font-weight: bold;
        color: aliceblue;
        background-color: rgb(32, 160, 255);
        //background-color: rgb(58, 58, 58);
        font-family: PingFang SC;
    }

    .group .editGroup {
        float: right;
    }

    .row-title {
        margin: 35px;
    }

    .addGroup {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
</style>
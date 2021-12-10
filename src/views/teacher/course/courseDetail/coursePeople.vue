<template>
  <div>
    <el-tabs v-model="activeName">
      <el-tab-pane label="所有人" name="first">
        <el-row>
          <el-col :span="3">
            <v-btn dark @click="handleDetailS">手动添加学生</v-btn></el-col
          >
          <el-col :span="3" :offset="1"
            ><v-btn dark @click="handleExcelS">表格导入学生</v-btn></el-col
          ><el-col :span="5" :offset="7">
            <v-text-field
              v-model="assist"
              filled
              label="助教"
              type="text"
              :readonly="true"
            ></v-text-field
          ></el-col>
          <el-col :span="3" :offset="2"
            ><v-btn @click="handleAssist" dark color="cyan"
              >设置助教</v-btn
            ></el-col
          ></el-row
        >

        <el-table :data="studentData" style="width: 100%">
          <el-table-column prop="s_id" label="学号" sortable />
          <el-table-column prop="name" label="姓名" sortable />
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="小组" name="second">
        <el-row>
          <el-col :span="3">
            <v-btn dark @click="handleDetailG">手动添加小组</v-btn></el-col
          >
          <el-col :span="3" :offset="1"
            ><v-btn dark @click="handleExcelT">表格导入小组</v-btn></el-col
          ></el-row
        >

        <v-expansion-panels focusable style="margin-top: 20px">
          <v-expansion-panel v-for="(data, index) in groupData" :key="index">
            <v-expansion-panel-header>
              {{ data.leader }}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <div v-for="(data, index) in data.member" :key="index">
                {{ data.name }}
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </el-tab-pane>
    </el-tabs>
    <el-dialog :visible.sync="dialogFormVisibleS" title="请输入学生信息" center>
      <el-form
        :model="formS"
        ref="formS"
        style="margin: 40px 65px 0px 25px"
        label-width="80px"
      >
        <el-form-item
          label="学号"
          :required="true"
          prop="s_id"
          status-icon="true"
        >
          <el-input v-model="formS.s_id"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisibleS = false">取消</el-button>
        <el-button type="primary" @click="addFromDetailS()">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogAssist"
      title="请选择助教"
      center
      width="300px"
    >
      <el-select v-model="assist">
        <el-option
          v-for="i in assistList"
          :key="i.ta_id"
          :label="i.ta_id"
          :value="i.ta_id"
        >
        </el-option>
      </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAssist = false">取消</el-button>
        <el-button type="primary" @click="setAssist()">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogFormVisibleG"
      title="请输入小组成员信息"
      center
    >
      <el-form
        ref="dynamicValidateForm"
        :model="dynamicValidateForm"
        style="margin: 40px 65px 0px 25px"
        label-width="80px"
      >
        <el-form-item
          prop="leader"
          label="组长"
          :rules="{
            required: true,
            message: 'id can not be null',
            trigger: 'blur',
          }"
        >
          <el-input v-model="dynamicValidateForm.leader"></el-input>
        </el-form-item>
        <el-form-item
          v-for="(domain, index) in dynamicValidateForm.members"
          :key="domain.key"
          :label="'学生' + index"
          :prop="'members.' + index + '.sid'"
          :rules="{
            required: true,
            message: 'id can not be null',
            trigger: 'blur',
          }"
        >
          <el-input v-model="domain.sid"></el-input
          ><el-button @click.prevent="removeDomain(domain)">移除</el-button>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="addFromDetailT('dynamicValidateForm')"
            >确定</el-button
          >
          <el-button @click="addDomain">新成员</el-button>
          <el-button @click="dialogFormVisibleG = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="dialogExcelVisibleS" title="请选择文件" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileListS"
        :multiple="true"
        :auto-upload="false"
        accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
      >
        <el-button type="primary">选取文件</el-button>
        <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogExcelVisibleS = false">取消</el-button>
        <el-button type="success" @click="addFromExcelS()">上传</el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogExcelVisibleG" title="请选择文件" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileListG"
        :multiple="true"
        :auto-upload="false"
        accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
      >
        <el-button type="primary">选取文件</el-button>
        <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogExcelVisibleG = false">取消</el-button>
        <el-button type="success" @click="addFromExcelG()">上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",

      activeName: "first",
      dialogFormVisibleS: false,
      dialogExcelVisibleS: false,
      dialogFormVisibleG: false,
      dialogExcelVisibleG: false,
      dialogAssist: false,

      studentData: [],
      groupData: [],

      assist: "",
      assistList: [],

      /*手动导入学生数据*/
      formS: {
        s_id: "",
      },
      /*手动导入小组成员数据*/
      dynamicValidateForm: {
        members: [
          {
            key: 1,
            sid: "",
          },
        ],
        leader: "",
      },
      fileListS: [],
      fileListG: [],

      currentPage: 1,
      pagesize: 6,
    };
  },
  methods: {
    handleDetailS() {
      this.dialogFormVisibleS = true;
    },
    handleExcelS() {
      this.dialogExcelVisibleS = true;
    },
    handleDetailG() {
      this.dialogFormVisibleG = true;
    },
    handleExcelT() {
      this.dialogExcelVisibleG = true;
    },
    handleAssist() {
      this.dialogAssist = true;
    },

    handlePreview(file) {
      console.log(file);
    },
    handleRemove(file, fileListS) {
      console.log(file, fileListS);
    },
    handleChange(file) {
      console.log(file);
      this.fileListS.push(file);
      console.log(this.fileListS);
    },
    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    addFromDetailS() {
      //手动增加学生
      var jsons = {
        class_id: this.c_id.toString(),
        s_id: this.formS.s_id,
        token: sessionStorage.getItem("token"),
      };
      console.log("手动增加学生");
      console.log(jsons);
      this.axios
        .post("/api/classAddStudentManually", JSON.stringify(jsons))
        .then((response) => {
          //这里使用了ES6的语法
          console.log("手动添加学生返回");
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else if (response.data["code"] === 401) {
            this.$message.warning("该学生已在班级中！");
          } else if (response.data["code"] === 402) {
            this.$message.warning("该学生不存在！");
          } else {
            if (response.data.code == "200") {
              this.dialogFormVisibleS = false;
              this.getStuList();
              this.$message({
                message: "添加成功",
                type: "success",
              });
              this.formS.s_id = "";
            }
          }
        });
    },

    addFromDetailT(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
          this.axios
            .post("", JSON.stringify(this.dynamicValidateForm))
            .then((response) => {
              //这里使用了ES6的语法
              console.log(response); //请求成功返回的数据
            });
          this.dialogFormVisibleG = false;
          //location.reload();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },

    addFromExcelS() {
      /*let fdParams = new FormData();
      this.fileListS.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      fdParams.append("userID", "123");

      this.axios
        .post("/api/file/addUser/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          timeout: 20000,
        })
        .then((response) => {
          console.log(response);
        })
        .catch({});

      this.dialogExcelVisibleS = false;*/
    },

    addFromExcelG() {
      /*let fdParams = new FormData();
      this.fileListG.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      fdParams.append("userID", "123");

      this.axios
        .post("/api/file/addUser/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          timeout: 20000,
        })
        .then((response) => {
          console.log(response);
        })
        .catch({});

      this.dialogExcelVisibleG = false;*/
    },

    setAssist() {
      //设置助教
      var jsons = {
        class_id: this.c_id.toString(),
        ta_id: this.assist,
        token: sessionStorage.getItem("token"),
      };
      console.log("设置助教");
      console.log(jsons);
      this.axios
        .post("/api/classAddTA", JSON.stringify(jsons))
        .then((response) => {
          console.log("setAssist");
          console.log(response);

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else if (response.data["code"] === 500) {
            this.$message.warning("该助教已经在班级中！");
          } else {
            this.$message({
              type: "success",
              message: "设置成功!",
            });
            this.dialogAssist = false;
          }
        });
    },
    removeDomain(item) {
      const index = this.dynamicValidateForm.members.indexOf(item);
      if (index !== -1) {
        this.dynamicValidateForm.members.splice(index, 1);
      }
    },
    addDomain() {
      this.dynamicValidateForm.members.push({
        key: Date.now(),
        sid: "",
      });
    },

    getStuList() {
      var jsons = {
        class_id: this.c_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/IDGetClassStudent", JSON.stringify(jsons))
        .then((response) => {
          console.log("getStu");
          console.log(response);

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.studentData = response.data.data["data"];
          }
        });
    },
    getAssistList() {
      console.log("获得助教");
      this.axios
        .get("/api/getUserInfo/getAllTA", {
          params: { token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("获得助教");

          this.assistList = response.data;
        });
    },
    getAssist() {
      //查看班级助教
    },

    getParams: function () {
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.c_id));
      console.log("cid===" + this.c_id);
    },
  },
  mounted() {
    this.getParams();
    this.getStuList();
    this.getAssistList();
    this.getAssist();
  },
};
</script>

<style scoped>
.box-card {
  border-radius: 15px;
  box-shadow: 7px 7px 10px rgba(0, 0, 0, 0.15);
}
.el-card {
  margin-bottom: 20px;
  margin-top: 15px;
}
</style>
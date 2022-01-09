<template>
  <div>
    <el-row>
      <el-col :span="3">
        <v-btn dark @click="handleDetailS">手动添加学生</v-btn></el-col
      >
      <el-col :span="3" :offset="1"
        ><v-btn dark @click="handleExcelS">表格导入学生</v-btn></el-col
      ><el-col :span="5" :offset="7">
        <v-text-field
          v-model="assist_name"
          filled
          label="助教"
          type="text"
          :readonly="true"
        ></v-text-field
      ></el-col>
      <el-col :span="3" :offset="2"
        ><v-btn @click="handleAssist" dark color="cyan">设置助教</v-btn></el-col
      ></el-row
    >

    <el-table :data="studentData" style="width: 100%">
      <el-table-column prop="s_id" label="学号" sortable />
      <el-table-column prop="name" label="姓名" sortable />
    </el-table>

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
      <el-select v-model="assist_id">
        <el-option
          v-for="i in assistList"
          :key="i.ta_id"
          :label="i.ta_id + i.name"
          :value="i.ta_id"
        >
        </el-option>
      </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAssist = false">取消</el-button>
        <el-button type="primary" @click="setAssist()">确定</el-button>
      </div>
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",

      dialogFormVisibleS: false,
      dialogExcelVisibleS: false,

      dialogAssist: false,

      studentData: [],
      groupData: [],

      assist_id: "",
      assist_name: "",
      assistList: [],

      /*手动导入学生数据*/
      formS: {
        s_id: "",
      },

      fileListS: [],
    };
  },
  methods: {
    handleDetailS() {
      this.dialogFormVisibleS = true;
    },
    handleExcelS() {
      this.dialogExcelVisibleS = true;
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

    addFromExcelS() {
      let fdParams = new FormData();
      this.fileListS.forEach((file) => {
        //console.log(file);
        fdParams.append("file", file.raw);
      });

      fdParams.append("class_id", this.c_id);
      fdParams.append("token", sessionStorage.getItem("token"));
      //console.log("addFromExcelS", this.fileListS);
      this.axios
        .post("/api/classAddStudentFile", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          //timeout: 20000,
        })
        .then((response) => {
          console.log("addFromExcelS", response);
          this.$message.success("添加成功");
          this.fileListS = [];
          this.dialogExcelVisibleS = false;
          this.getStuList();
        })
        .catch({});
    },

    setAssist() {
      //设置助教
      var jsons = {
        class_id: this.c_id.toString(),
        ta_id: this.assist_id,
        token: sessionStorage.getItem("token"),
      };

      this.axios
        .post("/api/classAddTA", JSON.stringify(jsons))
        .then((response) => {
          console.log("setAssist", response);

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
            this.getStuList();
            this.dialogAssist = false;
          }
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
          console.log("getStu", response);

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.studentData = response.data.data["data"];
            this.assist_id = response.data.data["ta_id"];
            this.assist_name = response.data.data["ta_name"];
          }
        });
    },
    getAssistList() {
      this.axios
        .get("/api/getUserInfo/getAllTA", {
          params: { token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("获得助教列表", response);

          this.assistList = response.data;
        });
    },

    getParams: function () {
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
    },
  },
  mounted() {
    this.getParams();
    this.getStuList();
    this.getAssistList();
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

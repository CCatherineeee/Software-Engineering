<template>
  <div>
    <el-row>
      <v-btn dark style="margin-bottom: 1%" @click="handleAddClass">
        新增班级
      </v-btn>
    </el-row>

    <el-row :gutter="8">
      <el-col v-for="item in classList" :key="item.class_id" :span="8">
        <v-card color="#385F73" dark>
          <div>
            <v-card-title v-text="item.class_id"></v-card-title>
            <v-card-subtitle v-text="item.t_name"></v-card-subtitle>
            <v-card-actions>
              <v-btn outlined rounded @click="handleTea(item)">
                设置教师
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="handleDeleteClass(item)"> 删除班级 </v-btn>
            </v-card-actions>
          </div>
        </v-card>
      </el-col>
    </el-row>

    <el-dialog
      :visible.sync="classDialog"
      title="新增班级"
      center
      width="300px"
    >
      <el-select v-model="tid">
        <el-option
          v-for="item in teaList"
          :key="item.id"
          :label="item.id + ' ' + item.name"
          :value="item.id"
        >
        </el-option>
      </el-select>

      <div slot="footer" class="dialog-footer">
        <el-button @click="classDialog = false">取消</el-button>
        <el-button type="primary" @click="createClass()">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="teaDialog" title="选择教师" center width="300px">
      <el-select v-model="changeTemp.t_id">
        <el-option
          v-for="i in teaList"
          :key="i.id"
          :label="i.id + i.name"
          :value="i.id"
        >
        </el-option>
      </el-select>
      <div slot="footer" class="dialog-footer">
        <el-button @click="teaDialog = false">取消</el-button>
        <el-button type="primary" @click="updateTea(changeTemp)"
          >确定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ManageClass",
  data() {
    return {
      classList: [],
      course_id: "",
      name: "",
      year: "",
      semester: "",
      id: "",
      teaList: [],
      changeTemp: {},
      tid: "",

      syllabus: "",
      teaDialog: false,
      proDialog: false,
      fileDialog: false,
      classDialog: false,
      exDialog: false,
      scoreDialog: false,
    };
  },
  methods: {
    getClasses() {
      var jsons = {
        courseID: this.course_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/showClass/", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.classList = response.data.data;
            console.log(this.classList);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    updateTea(row) {
      var jsons = {
        class_id: row.class_id,
        t_id: row.t_id,
        token: sessionStorage.getItem("token"),
      };
      console.log("更新教师");
      console.log(jsons);
      this.axios
        .post("/api/manageClass/changeTeacher", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getClasses();
            this.teaDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleDeleteClass(row) {
      this.$confirm("确认删除班级吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteClass(row);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          document.execCommand("Refresh");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },
    handleAddClass() {
      this.classDialog = true;
    },
    handleTea(item) {
      this.changeTemp = item;
      this.teaDialog = true;
    },

    createClass() {
      console.log("createClass", this.course_id);
      this.axios
        .post(
          "/api/manageClass/addClass",
          JSON.stringify({
            courseID: this.course_id,
            t_id: this.tid,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.classDialog = false;
            this.tid = "";
            this.getClasses();
          }
        });
    },
    deleteClass(row) {
      var jsons = {
        classID: row.class_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/deleteClass", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getClasses();
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getParams: function () {
      this.course_id = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).course_id;
      this.name = JSON.parse(this.$Base64.decode(this.$route.query.info)).name;
      this.year = JSON.parse(this.$Base64.decode(this.$route.query.info)).year;
      this.semester = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).semester;
      this.id = sessionStorage.getItem("id");
      console.log(this.course_id);
    },
    getTeaList() {
      //获得所有教师
      this.axios
        .get("/api/course/getAllTeacher/", {
          params: { token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getTeaList", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.teaList = response.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  mounted() {
    this.getParams();
    this.getClasses();
    this.getTeaList();
  },
};
</script>

<style scoped>
</style>

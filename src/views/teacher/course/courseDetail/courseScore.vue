<template>
  <el-tabs v-model="activeName">
    <el-tab-pane label="批改实验" name="first">
      <el-table
        :data="
          scoreData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
        <el-table-column sortable prop="name" label="姓名" sorted />
        <el-table-column sortable prop="id" label="学号" />
        <!-- 自定义列的遍历-->
        <el-table-column
          v-for="item in headers"
          :property="item.key"
          :key="item.key"
          :label="item.label"
          sortable
        >
          <!-- 数据的遍历  scope.row就代表数据的每一个对象-->
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="
                handleScore(
                  scope.row[scope.column.property],
                  scope.row.id,
                  scope.column.property
                )
              "
              >{{ scope.row[scope.column.property] }}</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-dialog
        :visible.sync="scoreDialog"
        title="请输入学生成绩"
        center
        width="300px"
      >
        <el-input v-model="score"></el-input>
        <div slot="footer" class="dialog-footer">
          <el-button @click="scoreDialog = false">取消</el-button>
          <el-button type="primary" @click="setScore()">确定</el-button>
        </div>
      </el-dialog>
    </el-tab-pane>
    <el-tab-pane label="查看报告" name="second">
      <el-table
        :data="
          scoreData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
        <el-table-column sortable prop="name" label="姓名" sorted />
        <el-table-column sortable prop="id" label="学号" />
        <!-- 自定义列的遍历-->
        <el-table-column
          v-for="item in headers"
          :property="item.key"
          :key="item.key"
          :label="item.label"
          sortable
        >
          <!-- 数据的遍历  scope.row就代表数据的每一个对象-->
          <template slot-scope="scope">
            <el-button
              type="text"
              @click="toReportOnline(scope)"
              v-if="item.type == '在线提交'"
              >查看</el-button
            >
            <el-button
              type="text"
              @click="checkReport(scope)"
              v-if="item.type == '提交文件'"
              >查看</el-button
            >
            <el-button
              type="text"
              @click="downReport(scope)"
              v-if="item.type == '提交文件'"
              >下载</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",
      scoreDialog: false,
      score: "",
      s_id: "",
      ex_id: "",

      activeName: "first",
      currentPage: 1,
      pagesize: 10,
      scoreData: [],
      headers: [],
      reportData: [],
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      console.log("cid", this.c_id);
    },
    handleScore(score, sid, ex_id) {
      console.log("handleScore", score, sid, ex_id);
      this.scoreDialog = true;
      this.score = score;
      this.s_id = sid;
      this.ex_id = ex_id.substring(ex_id.indexOf("_") + 1);
    },
    getScoreData() {
      var jsons = {
        class_id: this.c_id,
        token: sessionStorage.getItem("token"),
      };
      //console.log("getDatajsons", jsons);
      this.axios
        .post("/api/manageClass/GetClassStudentScore", JSON.stringify(jsons))
        .then((response) => {
          console.log("getScoreData", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            console.log("getScoreData", response.data.data);
            this.headers = response.data.data.experiment;
            this.scoreData = response.data.data.score;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setScore() {
      if (this.score > 100 || this.score < 0) {
        this.$message.warning("分数必须在0-100之间！");
        return;
      }
      var jsons = {
        s_id: this.s_id,
        ex_id: this.ex_id,
        score: this.score,
        t_id: this.id,
        token: sessionStorage.getItem("token"),
      };
      console.log(jsons);
      this.axios
        .post("/api/tea/Ex/scoreReport/", JSON.stringify(jsons))
        .then((response) => {
          console.log("setScore", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.$message.success("打分成功！");
            this.getScoreData();
            this.scoreDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    toReportOnline(row) {
      console.log("toReportOnline", row);
      const { href } = this.$router.resolve({
        path: "/teacherHome/concreteCourse/stuExperOnline",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({
              s_id: row.row.id,
              ex_id: row.column.property.replace("ex_", ""),
              score: row.row[row.column.property],
            })
          ),
        },
      });
      window.open(href, "_blank");
    },
    checkReport(row) {
      this.axios
        .post(
          "/api/Ex/showUpload/",
          JSON.stringify({
            s_id: row.row.id,
            ex_id: row.column.property.replace("ex_", ""),
          }),
          {
            responseType: "blob",
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((response) => {
          //var fname = row.filename
          //fname = decodeURIComponent(fname)
          //const title = fileName && (fileName.indexOf('filename=') !== -1) ? fileName.split('=')[1] : 'download';
          console.log("查看文件", response);
          if (response.data["type"] === "application/json") {
            this.$message.warning("该学生没有上传实验报告！");
          } else {
            const blob = new Blob([response.data], {
              type: "application/pdf",
            });
            //var downloadElement = document.createElement("a");
            var href = window.URL.createObjectURL(blob);
            window.open(href);
          }
        });
    },
    downReport(row) {
      console.log("downReport", row);
      console.log(row);
      let formData = new FormData();
      formData.append("s_id", row.row.id);
      formData.append("ex_id", row.column.property.replace("ex_", ""));

      this.axios
        .post("/api/tea/Ex/getReport/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then((response) => {
          console.log("downReport", response);
          if (response.data["type"] === "application/json") {
            this.$message.warning("该学生没有上传实验报告！");
          } else {
            const fileName = response.headers["content-disposition"];
            var fname = fileName.split("filename=")[1];
            fname = decodeURIComponent(fname);
            //const title = fileName && (fileName.indexOf('filename=') !== -1) ? fileName.split('=')[1] : 'download';

            const blob = new Blob([response.data], {
              type: "application/pdf",
            });
            var downloadElement = document.createElement("a");
            var href = window.URL.createObjectURL(blob);
            downloadElement.href = href;

            downloadElement.download = fname;
            document.body.appendChild(downloadElement);
            downloadElement.click();
            document.body.removeChild(downloadElement);
            window.URL.revokeObjectURL(href);
          }
        });
    },
  },
  mounted() {
    this.getParams();
    this.getScoreData();
  },
};
</script>

<style scoped>
.el-button--primary {
  color: white;
}
</style>

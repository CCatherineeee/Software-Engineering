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
            <el-button type="text" @click="checkReport(scope.row)"
              >查看</el-button
            >
            <el-button type="text" @click="downReport(scope.row)"
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
      scoreData: [
        {
          name: "lyw",
          id: "1951095",
          ex_1: "100",
          ex_2: "200",
          ex_3: "300",
          test: "400",
        },
        {
          name: "xzq",
          id: "1951104",
          ex_1: "100",
          ex_2: "200",
          ex_3: "300",
          test: "0",
        },
      ],
      headers: [
        {
          label: "实验1", //实验名字
          key: "ex_1", //实验id
        },
        {
          label: "实验2",
          key: "ex_2",
        },
        {
          label: "实验3",
          key: "ex_3",
        },
        {
          label: "实验4",
          key: "test",
        },
      ],
      reportData: [
        {
          name: "lyw",
          id: "1951095",
          ex_1: "100",
          ex_2: "200",
          ex_3: "300",
          test: "400",
        },
        {
          name: "xzq",
          id: "1951104",
          ex_1: "100",
          ex_2: "200",
          ex_3: "300",
          test: "0",
        },
      ],
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
    getData() {
      var jsons = {
        class_id: JSON.stringify(this.c_id),

        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/GetClassStudentScore", JSON.stringify(jsons))
        .then((response) => {
          console.log("getData", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.headers = response.data.data.experiment;
            this.scoreData = response.data.data.score;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setScore() {
      var jsons = {
        s_id: this.s_id,
        ex_id: this.ex_id,
        score: this.score,
        //t_id: this.id,
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
            this.getData();
            this.scoreDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    checkReport(row) {
      this.axios
        .post(
          "/api/manageClassFileRoute/download/",
          JSON.stringify({
            id: row.id,
            class_id: this.c_id,
            token: sessionStorage.getItem("token"),
          }),
          {
            responseType: "blob",
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            //const title = fileName && (fileName.indexOf('filename=') !== -1) ? fileName.split('=')[1] : 'download';

            const blob = new Blob([response.data], {
              type: "application/pdf",
            });
            var href = window.URL.createObjectURL(blob);
            window.open(href);
          }
        });
    },
    downReport(row) {
      this.axios
        .post(
          "/api/manageClassFileRoute/download/",
          JSON.stringify({
            id: row.id,
            class_id: this.class_id,
            token: sessionStorage.getItem("token"),
          }),
          {
            responseType: "blob",
          }
        )
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            var fname = row.filename;
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
    this.getData();
  },
};
</script>


<template>
  <div>
    <el-card>
      <el-table
        ref="filterTable"
        @selection-change="handleSelectionChange"
        :data="
          stuExData.filter(
            (data) =>
              !search ||
              data.sid.toLowerCase().includes(search.toLowerCase()) ||
              data.name.toLowerCase().includes(search.toLowerCase())
          )
        "
        style="width: 100%"
      >
        <el-table-column prop="s_id" label="学号" sortable />
        <el-table-column prop="s_name" label="姓名" sortable />
        <el-table-column prop="status" label="是否提交" sortable />
        <el-table-column prop="submitTime" label="提交日期" sortable />
        <el-table-column prop="score" label="分数" sortable />

        <el-table-column>
          <template #header>
            <el-input v-model="search" placeholder="请输入" />
          </template>
          <template #default="scope">
            <v-row>
              <v-col cols="3" v-if="ex_type == '在线提交'">
                <v-btn small dark @click="giveScoreOnline(scope.row)"
                  >查看</v-btn
                >
              </v-col>
              <v-col cols="4" v-if="ex_type == '提交文件'">
                <v-btn
                  small
                  dark
                  @click="check(scope.row)"
                  v-if="scope.row.status == '是'"
                  >查看</v-btn
                >
              </v-col>
              <v-col cols="4" v-if="ex_type == '提交文件'">
                <v-btn
                  small
                  dark
                  @click="download(scope.row)"
                  v-if="scope.row.status == '是'"
                  >下载</v-btn
                >
              </v-col>
              <v-col cols="4" v-if="ex_type == '提交文件'">
                <v-btn small dark @click="handleScoreDown(scope.row)"
                  >打分</v-btn
                >
              </v-col>
            </v-row>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pagesize"
        layout="total,  prev, pager, next, jumper"
        :total="stuExData.length"
        filterState
      >
      </el-pagination>
    </el-card>
    <el-dialog
      :visible.sync="scoreDialog"
      title="学生分数"
      center
      width="300px"
    >
      <el-input v-model="stuScore"></el-input>
      <div slot="footer" class="dialog-footer">
        <el-button @click="proDialog = false">取消</el-button>
        <el-button type="primary" @click="giveScoreDown()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script >
export default {
  data() {
    return {
      ex_id: "",
      ex_type: "",
      search: "",
      currentPage: 1,
      scoreDialog: false,
      stuScore: "",
      s_id: "",

      pagesize: 6,
      multipleSelection: [],

      stuExData: [
        { sid: "1", name: "1", submit: "2021.11.1", score: "2022.2.2" },
      ],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleScoreDown(row) {
      this.scoreDialog = true;
      this.s_id = row.s_id;
    },
    giveScoreDown() {
      var jsons = {
        s_id: this.s_id,
        ex_id: this.ex_id,
        score: this.stuScore,
        ta_id: sessionStorage.getItem("id"),
        token: sessionStorage.getItem("token"),
      };
      console.log(jsons);
      this.axios
        .post("/api/tea/Ex/taScoreReport/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.$message.success("成功打分！");
            this.scoreDialog = false;
            this.stuScore = "";
            this.getStuEx();
          }
        });
    },

    giveScoreOnline(row) {
      this.$router.push({
        path: "/assistHome/concreteCourse/stuExper",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({
              s_id: row.s_id,
              ex_id: this.ex_id,
              score: row.score,
            })
          ),
        },
      });
    },

    check(row) {
      //console.log("checkjson", row, this.ex_id);
      this.axios
        .post(
          "/api/Ex/showUpload/",
          JSON.stringify({
            s_id: row.s_id,
            ex_id: this.ex_id.toString(),
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

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            console.log("查看文件", response);
            //const fileName = response.headers["content-disposition"];
            //var fname = fileName.split("filename=")[1];
            //fname = decodeURIComponent(fname);
            const blob = new Blob([response.data], {
              type: "application/pdf",
            });
            //var downloadElement = document.createElement("a");
            var href = window.URL.createObjectURL(blob);
            window.open(href);
          }
        });
    },
    download(row) {
      //console.log(row);
      let formData = new FormData();
      formData.append("s_id", row.s_id);
      formData.append("ex_id", this.ex_id);

      this.axios
        .post("/api/tea/Ex/getReport/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        })
        .then((response) => {
          console.log("download", response);

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
          /*
        href.href = window.URL.createObjectURL(blob);
        href.target = "_blank";
        href.click();
          */
          //console.log(response)
        });
    },
    getStuEx() {
      this.axios
        .post(
          "/api/tea/Ex/getReportList/",
          JSON.stringify({
            ex_id: this.ex_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("stuEx", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.stuExData = response.data.data;
          }
        });
    },
    getParams: function () {
      this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "ex_id"
      ];
      this.ex_type = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "ex_type"
      ];
    },
  },
  mounted() {
    this.getParams();
    this.getStuEx();
  },
};
</script>
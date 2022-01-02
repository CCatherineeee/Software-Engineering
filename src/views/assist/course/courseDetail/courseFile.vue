<template>
  <div>
    <el-table
      ref="filterTable"
      row-key="id"
      :data="
        fileData.filter(
          (data) =>
            !search ||
            data.title.toLowerCase().includes(search.toLowerCase()) ||
            data.upload.toLowerCase().includes(search.toLowerCase()) ||
            data.modify.toLowerCase().includes(search.toLowerCase()) ||
            data.author.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
    >
      <el-table-column prop="filename" label="文件名" sortable />
      <el-table-column prop="date" label="上传时间" sortable />

      <el-table-column>
        <template #header>
          <el-input v-model="search" />
        </template>
        <template #default="scope">
          <v-row>
            <v-col cols="3">
              <v-btn dark small color="pink" @click="handleCheck(scope.row)"
                >查看</v-btn
              >
            </v-col>
            <v-col cols="3">
              <v-btn dark small color="indigo" @click="handleDown(scope.row)"
                >下载</v-btn
              ></v-col
            >
          </v-row>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="fileData.length"
    >
    </el-pagination>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      currentPage: 1,
      pagesize: 6,

      c_id: "",

      fileData: [],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },

    handleCheck(row) {
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
    handleDown(row) {
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

    getFileList() {
      this.axios
        .post(
          "/api/manageClassFileRoute/getClassFile",
          JSON.stringify({
            class_id: this.c_id,
            token: sessionStorage.getItem("token"),
          })
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
            this.fileData = response.data.data;
          }
        });
    },
    getParams: function () {
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      console.log("cid===" + this.c_id);
    },
  },
  mounted() {
    this.getParams();
    this.getFileList();
  },
};
</script>

<style scoped>
.el-divider--vertical {
  display: inline-block;
  width: 1px;
  height: 100%;
  margin: 0 8px;
  vertical-align: middle;
  position: relative;
}
</style>

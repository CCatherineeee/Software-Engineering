<template>
  <div>
    <v-btn dark @click="handleUpload">上传文件</v-btn>
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
            <v-col cols="3">
              <v-btn dark small @click="handleDelete(scope.row)"
                >删除</v-btn
              ></v-col
            ></v-row
          >
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

    <el-dialog :visible.sync="fileDialog" title="请选择文件" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileList"
        :multiple="true"
        :auto-upload="false"
        accept=""
      >
        <el-button type="primary">选取文件</el-button>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="fileDialog = false">取消</el-button>
        <el-button type="success" @click="uploadFile()">上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      currentPage: 1,
      pagesize: 6,
      fileDialog: false,
      c_id: "",

      fileData: [],
      fileList: [],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handlePreview(file) {
      console.log(file);
    },

    handleRemove(file) {
      this.fileList.pop(file);
    },

    handleChange(file) {
      this.fileList.push(file);
    },

    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    handleUpload() {
      this.fileDialog = true;
    },
    handleCheck(row) {
      this.axios
        .post(
          "/api/manageClassFileRoute/preview/",
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
            const blob = new Blob([response.data], {
              type: "application/pdf",
            });
            //var downloadElement = document.createElement("a");
            var href = window.URL.createObjectURL(blob);
            window.open(href);
          }
        });
    },
    handleDown(row) {
      console.log(row);
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
    handleDelete(row) {
      this.$confirm("确认删除吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteFile(row);
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },

    uploadFile() {
      console.log(this.fileList);
      let param = new FormData();
      this.fileList.forEach((file) => {
        param.append("files", file.raw);
      });
      param.append("class_id", this.c_id);
      param.append("token", sessionStorage.getItem("token"));
      this.axios
        .post("/api/manageClassFileRoute/addFile", param, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
        })
        .then((res) => {
          console.log(res);
          if (res.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (res.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            if (res.data["status"] === 200) {
              this.$message("上传成功");
              this.fileList = [];
              this.fileDialog = false;
              this.getFileList();
            } else {
              this.$message("上传失败");
            }
          }
        });
    },
    deleteFile(row) {
      this.axios
        .post(
          "/api/manageClassFileRoute/deleteClassFile",
          JSON.stringify({
            class_id: this.c_id,
            id: row.id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((res) => {
          console.log(res);
          if (res.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (res.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            if (res.data["status"] === 200) {
              this.$message("删除成功");
              this.getFileList();
            } else {
              this.$message(res.data["message"]);
            }
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
.el-button--primary {
  color: white;
}
.el-button--success {
  color: white;
}
</style>

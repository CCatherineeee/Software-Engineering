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
      <el-table-column prop="title" label="文件名" sortable />
      <el-table-column prop="upload" label="上传时间" sortable />
      <el-table-column prop="modify" label="修改时间" sortable />
      <el-table-column prop="author" label="修改者" sortable />

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

      fileData: [
        {
          title: "wenjian1",
          upload: "1",
          modify: "1",
          author: "1",
        },
      ],
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
    handleUpload() {
      this.fileDialog = true;
    },
    handleCheck() {},
    handleDown(row) {
      console.log(row);
    },
    handleDelete(row) {
      this.$confirm("确认删除吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteFile(row);

          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },

    uploadFile() {
      //上传文件
    },
    deleteFile(row) {
      //删除文件
      console.log(row);
    },
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

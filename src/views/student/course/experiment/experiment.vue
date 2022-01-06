<template>
  <div>
    <div
      style="margin: auto auto; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.15)"
    >
      <el-descriptions
        direction="vertical"
        :column="1"
        border
        size="medium"
        title="实验指导"
      >
        <template slot="extra">
          <el-row :gutter="20">
            <el-col :span="10" v-if="ex_info.status == '未截止'"
              ><v-btn
                dark
                v-if="ex_info.ex_type == '在线提交'"
                @click="fillExperiment()"
              >
                填写 </v-btn
              ><v-btn
                dark
                v-if="ex_info.ex_type == '提交文件'"
                @click="handleFile"
              >
                上传
              </v-btn></el-col
            >

            <el-col :span="14"><v-btn dark @click="back">返回</v-btn></el-col>
          </el-row>
        </template>
        <el-descriptions-item label="实验名称">{{
          ex_info.title
        }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{
          ex_info.create_time
        }}</el-descriptions-item>
        <el-descriptions-item label="截止日期">{{
          ex_info.end_time
        }}</el-descriptions-item>
        <el-descriptions-item label="实验权重" :span="2">{{
          ex_info.weight
        }}</el-descriptions-item>
        <el-descriptions-item label="实验状态">{{
          ex_info.status
        }}</el-descriptions-item>

        <el-descriptions-item label="实验简介">{{
          ex_info.brief
        }}</el-descriptions-item>
      </el-descriptions>
    </div>

    <el-dialog
      :visible.sync="dialogVisible"
      title="请选择文件"
      center
      border-radius="4px"
    >
      <el-upload
        ref="uploadImport"
        action=""
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileList"
        :multiple="true"
        :auto-upload="false"
        accept=""
      >
        <el-button type="primary" style="float: center">选取文件</el-button>
        <div slot="tip" class="el-upload__tip"></div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="success" @click="uploadMyEx()">上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogVisible: false,
      dialog: false,
      fileList: [],
      ex_id: "",
      ex_info: {},
    };
  },
  methods: {
    getParams: function () {
      this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info));
    },

    back() {
      this.$router.go(-1);
    },

    handleFile() {
      this.dialogVisible = true;
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
    fillExperiment() {
      this.$router.push({
        path: "/studentHome/concreteCourse/FillExper",
        query: {
          info: this.$Base64.encode(JSON.stringify(this.ex_info.ex_id)),
          title: this.$Base64.encode(JSON.stringify(this.ex_info.title)),
        },
      });
    },
    getExInfo() {
      var jsons = {
        ex_id: this.ex_id,
      };
      this.axios
        .post("/api/course/getExById/", JSON.stringify(jsons))
        .then((response) => {
          //这里使用了ES6的语法
          //this.tableData = response.data
          console.log("getExInfo");
          console.log(response);
          if (response.data.data.status == 0)
            response.data.data.status = "未发布";
          if (response.data.data.status == 1)
            response.data.data.status = "未截止";
          if (response.data.data.status == 3)
            response.data.data.status = "已截止";
          this.ex_info = response.data.data;
        });
    },
    uploadMyEx() {
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
  },
  mounted() {
    this.getParams();
    this.getExInfo();
  },
};
</script>


<style scoped>
.el-row {
  margin: 20px;
}

.bg-purple {
  background: #385fbb;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
  margin: 5px, 5px, 5px, 5px;
  padding: 5px, 5px, 5px, 5px;
}
</style>


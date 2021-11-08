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
            <el-col :span="10"><v-btn dark> 导出 </v-btn></el-col>
            <el-col :span="5"><v-btn dark @click="back">返回</v-btn></el-col>
          </el-row>
        </template>
        <el-descriptions-item label="实验名称"
          >kooriookami</el-descriptions-item
        >
        <el-descriptions-item label="实验目的"
          >18100000000</el-descriptions-item
        >
        <el-descriptions-item label="实验设备" :span="2"
          >苏州市</el-descriptions-item
        >

        <el-descriptions-item label="实验步骤"
          >江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item
        >
      </el-descriptions>
    </div>

    <el-row :gutter="10">
      <el-col :span="6" :offset="6"
        ><v-btn dark @click="fillExperiment">在线填写报告</v-btn></el-col
      >
      <el-col :span="6"
        ><v-btn dark @click="handleFile">上传报告文件</v-btn></el-col
      >
    </el-row>

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
        <el-button type="success">上传</el-button>
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
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内
      console.log("传来的参数==" + routerParams);
      this.id = routerParams;
    },

    back() {
      this.$router.push("/home/concreteCourse/Exper");
    },
    fillExperiment() {
      this.$router.push("/home/concreteCourse/FillExper");
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
  },
  mounted() {
    this.getParams();
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


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
        title="实验信息"
      >
        <template slot="extra">
          <el-row :gutter="20">
            <el-col :span="7"><v-btn dark @click="back">返回</v-btn></el-col>
          </el-row>
        </template>
        <el-descriptions-item label="实验名称">{{
          ex_info.title
        }}</el-descriptions-item>
        <el-descriptions-item label="截止日期">{{
          ex_info.end_time
        }}</el-descriptions-item>
        <el-descriptions-item label="实验权重" :span="2">{{
          ex_info.weight
        }}</el-descriptions-item>

        <el-descriptions-item label="实验简介">{{
          ex_info.brief
        }}</el-descriptions-item>
      </el-descriptions>
    </div>
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


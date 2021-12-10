<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-textarea
          filled
          label="实验名称"
          disabled
          auto-grow
          height="20px"
          :value="ex_info.title"
        ></v-textarea>
      </v-col>
      <v-col cols="12" md="6">
        <v-textarea
          filled
          label="实验时间"
          auto-grow
          height="20px"
          value=""
        ></v-textarea>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-textarea
          filled
          label="实验地点"
          auto-grow
          height="20px"
          value=""
        ></v-textarea>
      </v-col>
      <v-col cols="12" md="6">
        <v-textarea
          filled
          label="合作人员"
          auto-grow
          height="20px"
          value=""
        ></v-textarea>
      </v-col>
    </v-row>
    <v-textarea filled label="实验目的" auto-grow value=""></v-textarea>

    <v-textarea filled label="实验设备" auto-grow value=""></v-textarea>

    <v-textarea filled label="实验步骤" auto-grow value=""></v-textarea>

    <v-textarea filled label="实验过程" auto-grow value=""></v-textarea>

    <v-textarea filled label="结果分析" auto-grow value=""></v-textarea>
    <el-row :gutter="10">
      <el-col :span="3" :offset="6"><v-btn dark>提交</v-btn></el-col>
      <el-col :span="3"><v-btn dark>暂存</v-btn></el-col>
      <el-col :span="3"><v-btn dark @click="back">取消</v-btn></el-col>
    </el-row>
  </v-container>
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
      // 取到路由带过来的参数
      this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info));
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
    back() {
      this.$router.go(-1);
    },
  },
  mounted() {
    this.getParams();
    this.getExInfo();
  },
};
</script>
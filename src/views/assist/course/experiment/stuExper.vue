<template>
  <div>
    <div
      style="margin: auto auto; box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.15)"
    >
      <el-row :gutter="20">
        <el-col :span="6">
          <v-textarea
            label="score"
            auto-grow
            outlined
            rows="1"
            row-height="15"
            v-model="score"
          ></v-textarea
        ></el-col>
        <el-col :span="2" :offset="14"
          ><v-btn dark @click="confirm"> 确认 </v-btn></el-col
        >
        <el-col :span="2"><v-btn dark @click="back">返回</v-btn></el-col>
      </el-row>
      <el-descriptions
        direction="vertical"
        :column="1"
        border
        size="medium"
        title="学号姓名"
      >
        <el-descriptions-item label="实验名称">{{
          ex_info.title
        }}</el-descriptions-item>
        <el-descriptions-item label="实验目的"
          >18100000000</el-descriptions-item
        >
        <el-descriptions-item label="实验设备" :span="2"
          >苏州市</el-descriptions-item
        >

        <el-descriptions-item label="实验步骤"
          >江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item
        >
        <el-descriptions-item label="结果分析"
          >江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item
        >
      </el-descriptions>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      s_id: "",
      ex_id: "",
      name: "",
      score: "",
      exReport: {},
      ex_info: {},
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      this.s_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "s_id"
      ];
      this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "ex_id"
      ];
      this.score = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "score"
      ];
    },

    confirm() {
      this.axios
        .post(
          "/api/tea/Ex/scoreReport/",
          JSON.stringify({
            s_id: this.s_id,
            ex_id: this.ex_id,
            score: this.score,
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
            this.$message.success("成功打分！");
          }
        });
    },

    back() {
      this.$router.go(-1);
    },
    getExReport() {},
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


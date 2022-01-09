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
        :title="s_id"
      >
        <el-descriptions-item label="实验名称">{{
          exReport.title
        }}</el-descriptions-item>
        <el-descriptions-item label="实验目的">{{
          exReport.goal
        }}</el-descriptions-item>
        <el-descriptions-item label="实验设备" :span="2">{{
          exReport.device
        }}</el-descriptions-item>

        <el-descriptions-item label="实验步骤">{{
          exReport.step
        }}</el-descriptions-item>
        <el-descriptions-item label="实验过程">{{
          exReport.process
        }}</el-descriptions-item>
        <el-descriptions-item label="结果分析">{{
          exReport.result
        }}</el-descriptions-item>
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
      exReport: {
        title: "",
        goal: "",
        device: "",
        step: "",
        process: "",
        result: "",
      },
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
      console.log(
        "getParams",
        JSON.parse(this.$Base64.decode(this.$route.query.info))
      );
    },

    confirm() {
      if (this.score > 100 || this.score < 0) {
        this.$message.warning("分数必须在0-100之间！");
        return;
      }
      this.axios
        .post(
          "/api/tea/Ex/taScoreReport/",
          JSON.stringify({
            s_id: this.s_id,
            ex_id: this.ex_id,
            score: this.score,
            ta_id: sessionStorage.getItem("id"),
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("confirm", response);
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

    getExReport() {
      var jsons = {
        ex_id: this.ex_id,
        s_id: this.s_id,
      };

      this.axios
        .post("/api/Ex/checkFilled", JSON.stringify(jsons))
        .then((response) => {
          //这里使用了ES6的语法
          //this.tableData = response.data

          console.log("getExReport", response);

          this.exReport.title = response.data.data.title;
          this.exReport.goal = response.data.data.goal
            .replace("<p>", "")
            .replace("</p>", "");
          this.exReport.device = response.data.data.device
            .replace("<p>", "")
            .replace("</p>", "");
          this.exReport.step = response.data.data.step
            .replace("<p>", "")
            .replace("</p>", "");
          this.exReport.process = response.data.data.process
            .replace("<p>", "")
            .replace("</p>", "");
          this.exReport.result = response.data.data.result
            .replace("<p>", "")
            .replace("</p>", "");
        });
    },
  },
  mounted() {
    this.getParams();
    this.getExReport();
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


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
          ></v-textarea
        ></el-col>
        <el-col :span="2" :offset="14" @click="confirm"
          ><v-btn dark> 确认 </v-btn></el-col
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
      sid: "",
      name: "",
      score: "",
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

    confirm() {},

    back() {
      this.$router.push("/teacherHome/concreteCourse/stuExperList");
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


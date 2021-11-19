<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-textarea
          filled
          label="实验名称"
          auto-grow
          height="20px"
          value=""
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
      this.$router.push("/studentHome/concreteCourse/ConExper");
    },
  },
  mounted() {
    this.getParams();
  },
};
</script>
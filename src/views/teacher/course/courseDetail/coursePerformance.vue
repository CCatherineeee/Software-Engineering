<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="具体成绩" name="first">具体成绩?可能不需要</el-tab-pane>
    <el-tab-pane label="成绩分析" name="second">成绩分析</el-tab-pane>
  </el-tabs>
</template>
<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",

      activeName: "first",
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
          "class_id"
          ];
    },
  },
  mounted() {
    this.getParams();
  },
};
</script>

<template>
  <el-container style="margin-top: 20px">
    <el-header>
      <el-menu @select="handleSelect" mode="horizontal">
        <el-menu-item index="/studentHome/concreteCourse/examHome/checkExam">
          <span slot="title">查看测验</span>
        </el-menu-item>
      </el-menu>
    </el-header>
    <el-main> <router-view></router-view></el-main>
  </el-container>
</template>

<script>
export default {
  name: "examHome",
  data() {
    return {
      course_id: "",
    };
  },
  methods: {
    getParams() {
      var class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      this.course_id = class_id.substring(0, 13);
    },
    handleSelect(index) {
      this.$router.push({
        path: index,
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ class_id: this.class_id })
          ),
        },
      });
    },
  },
  mounted() {
    this.getParams();
  },
};
</script>

<style scoped>
.el-button--primary {
  color: white;
}
</style>
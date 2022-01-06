<template>
  <el-container style="margin-top: 20px">
    <el-header>
      <el-menu @select="handleSelect" mode="horizontal">
        <el-menu-item index="/teacherHome/concreteCourse/examHome/checkExam">
          <span slot="title">查看测验</span>
        </el-menu-item>
        <el-menu-item index="/teacherHome/concreteCourse/examHome/addExam">
          <span slot="title">新增测验</span>
        </el-menu-item>

        <el-menu-item index="/teacherHome/concreteCourse/examHome/analysisExam">
          <span slot="title">测验分析</span>
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
    getParams: function () {
      this.course_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "course_id"
      ];
    },
    handleSelect(index) {
      this.$router.push({
        path: index,
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ course_id: this.course_id })
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
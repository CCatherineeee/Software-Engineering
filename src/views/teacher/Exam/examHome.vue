<template>
  <el-container style="margin-top: 20px">
    <el-header>
      <el-menu @select="handleSelect" mode="horizontal">
        <el-menu-item index="/teacherHome/duty-course/courseInfo">
          <span slot="title">课程信息管理</span>
        </el-menu-item>
        <el-menu-item index="/teacherHome/duty-course/manageEx">
          <span slot="title">实验管理</span>
        </el-menu-item>
        <el-menu-item index="/teacherHome/duty-course/manageClass">
          <span slot="title">班级管理</span>
        </el-menu-item>
        <el-menu-item index="/teacherHome/duty-course/exam/checkExam">
          <span slot="title">查看测验</span>
        </el-menu-item>
        <el-menu-item index="/teacherHome/duty-course/exam/addExam">
          <span slot="title">新增测验</span>
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
      name: "",
      year: "",
      semester: "",
      id: "",
    };
  },
  methods: {
    getParams: function () {
      this.course_id = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).course_id;
      this.name = JSON.parse(this.$Base64.decode(this.$route.query.info)).name;
      this.year = JSON.parse(this.$Base64.decode(this.$route.query.info)).year;
      this.semester = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).semester;
      this.id = sessionStorage.getItem("id");
    },
    handleSelect(index) {
      this.$router.push({
        path: index,
        query: {
          info: this.$Base64.encode(
            JSON.stringify({
              course_id: this.course_id,
              name: this.name,
              year: this.year,
              semester: this.semester,
            })
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

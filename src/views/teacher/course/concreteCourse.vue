<template>
  <el-container class="back">
    <el-header class="hBack">{{ course_name }}</el-header>
    <el-container>
      <el-aside width="120px" class="lBack">
        <el-menu @select="handleSelect">
          <el-menu-item index="/teacherHome/concreteCourse/Ann">
            <span slot="title">公告</span>
          </el-menu-item>
          <el-menu-item index="/teacherHome/concreteCourse/Exper">
            <span slot="title">实验</span>
          </el-menu-item>

          <el-menu-item index="/teacherHome/concreteCourse/Perform">
            <span slot="title">成绩</span>
          </el-menu-item>
          <el-menu-item index="/teacherHome/concreteCourse/Score">
            <span slot="title">批改</span>
          </el-menu-item>
          <el-menu-item index="/teacherHome/concreteCourse/Peo">
            <span slot="title">人员</span>
          </el-menu-item>
          <el-menu-item index="/teacherHome/concreteCourse/File">
            <span slot="title">文件</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="mBack"> <router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.back {
  background: rgb(255, 255, 255);
  border-radius: 15px;
  height: 700px;
  margin-top: 20px;
}
.hBack {
  padding: 20px;
  text-align: left;
  font: 20px Microsoft YaHei;
}
.lBack {
  padding: 20px;
  border-radius: 15px;
}
.mBack {
  padding: 20px;
  border-radius: 15px;
  box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15);
}
.rBack {
  padding: 20px;
}
</style>


<script>
export default {
  data() {
    return {
      c_id: "",
      course_name: "",
    };
  },
  methods: {
    getParams: function () {
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
    },
    getClassInfo() {
      var jsons = {
        class_id: this.c_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/IDGetClass", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.course_name = response.data.data.course_name;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleSelect(index) {
      this.$router.push({
        path: index,
        query: {
          info: this.$Base64.encode(JSON.stringify({ class_id: this.c_id })),
        },
      });
    },
  },
  mounted() {
    this.getParams();
    this.getClassInfo();
  },
};
</script>

<template>
  <el-container class="back">
    <el-header class="hBack">{{ course_name }}</el-header>
    <el-container>
      <el-aside width="120px" class="lBack">
        <el-menu @select="handleSelect">
          <el-menu-item index="/studentHome/concreteCourse/Ann">
            <span slot="title">公告</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Exper">
            <span slot="title">实验</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Perform">
            <span slot="title">成绩</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Peo">
            <span slot="title">人员</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/File">
            <span slot="title">文件</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/examHome/checkExam">
            <span slot="title">测验</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="mBack"> <router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: "",
      class_id: "",
      course_name: "",
    };
  },
  methods: {
    getParams: function () {
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
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
    getClassInfo() {
      var jsons = {
        class_id: this.class_id,
        token: sessionStorage.getItem("token"),
      };

      this.axios
        .post("/api/manageClass/IDGetClass", JSON.stringify(jsons))
        .then((response) => {
          console.log(this.response);
          console.log(response.data["data"]);
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
  },
  mounted() {
    this.getParams();
    this.getClassInfo();
    console.log(this.class_id);
  },
};
</script>
<style scoped>
.back {
  background: rgb(255, 255, 255);
  border-radius: 15px;
  height: 800px;
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

<template>
  <div>
    <el-table :data="studentData" style="width: 100%">
      <el-table-column prop="s_id" label="学号" sortable />
      <el-table-column prop="name" label="姓名" sortable />
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",

      studentData: [],

      currentPage: 1,
      pagesize: 6,
    };
  },
  methods: {
    getStuList() {
      var jsons = {
        class_id: this.c_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/IDGetClassStudent", JSON.stringify(jsons))
        .then((response) => {
          console.log("getStu");
          console.log(response);

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.studentData = response.data.data["data"];
          }
        });
    },

    getParams: function () {
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
    },
  },
  mounted() {
    this.getParams();
    this.getStuList();
  },
};
</script>

<style scoped>
.box-card {
  border-radius: 15px;
  box-shadow: 7px 7px 10px rgba(0, 0, 0, 0.15);
}
.el-card {
  margin-bottom: 20px;
  margin-top: 15px;
}
</style>

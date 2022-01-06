<template>
  <el-card
    style="
      box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15);
      margin-left: 15%;
      margin-right: 15%;
    "
  >
    <el-form
      ref="userAccount"
      style="margin: 40px 100px 0px 50px"
      :model="userAccount"
      label-width="80px"
    >
      <el-form-item label="姓名" prop="name">
        <el-input type="text" v-model="userAccount.name"></el-input>
      </el-form-item>

      <el-form-item label="学号" prop="ta_id">
        <el-input v-model="userAccount.ta_id" :disabled="true"></el-input>
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input type="email" v-model="userAccount.email"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button style="margin-left: 80px" @click="save()" type="primary"
          >保存修改</el-button
        >
        <el-button style="margin-left: 100px" @click="back">取消</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      userAccount: {},
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    save() {
      var jsons = {
        name: this.userAccount.name,
        ta_id: this.userAccount.ta_id,

        email: this.userAccount.email,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/editInfo/TA/", JSON.stringify(jsons))
        .then((response) => {
          console.log("save", response);

          if (response.data == "Success")
            this.$message({
              message: "修改成功",
              type: "success",
            });
          else this.$message.error("错误");
          this.getTaInfo();
        });
    },
    back() {
      this.$router.go(-1);
    },
    getTaInfo() {
      this.axios
        .get("/api/getUserInfo/TA/", {
          params: { ta_id: this.id },
          crossDomain: true,
        })
        .then((response) => {
          console.log();
          console.log("助教信息", response);

          this.userAccount = response.data[0];
        })
        .catch(function (error) {
          console(error);
        });
    },
  },
  mounted() {
    this.getParams();
    this.getTaInfo();
  },
};
</script>

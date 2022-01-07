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

      <el-form-item label="工号" prop="admin_id">
        <el-input v-model="userAccount.admin_id" :disabled="true"></el-input>
      </el-form-item>

      <el-form-item label="手机" prop="phone_number">
        <el-input v-model="userAccount.phone_number"></el-input>
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
      id: "",
      userAccount: {
        name: "",
        admin_id: 111,
        phone: 111,
        email: "",
      },
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      //var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内

      this.id = JSON.parse(this.$Base64.decode(this.$route.query.info));

      console.log("路有参数" + this.id);
    },
    getAdminInfo() {
      this.axios
        .get("/api/getAdminInfo/admin/", {
          params: { admin_id: this.id, token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getAdminInfo");
          console.log(response);
          this.userAccount = response.data[0];
        })
        .catch(function (error) {
          console(error);
        });
    },

    save() {
      if (this.userAccount.phone_number.length != 11) {
        this.$message.warning("请输入11位的手机号！");
        return;
      }

      var jsons = {
        name: this.userAccount.name,
        admin_id: this.userAccount.admin_id,
        phone_number: this.userAccount.phone_number,
        email: this.userAccount.email,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/editInfo/Admin/", JSON.stringify(jsons))
        .then((response) => {
          console.log("save");
          console.log(response);

          if (response.data == "Success")
            this.$message({
              message: "修改成功",
              type: "success",
            });
          else this.$message.error("错误");
        })
        .catch((error) => {
          this.$message("网络错误！");
          console.log(error);
        });
    },
    back() {
      this.$router.go(-1);
    },
  },
  mounted() {
    this.getParams();
    this.getAdminInfo();
  },
};
</script>

<style scoped>
.el-button--primary {
  color: white;
}
</style>

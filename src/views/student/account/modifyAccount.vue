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

      <el-form-item label="学号" prop="sid">
        <el-input v-model="userAccount.sid" :disabled="true"></el-input>
      </el-form-item>

      <el-form-item label="学院" prop="college">
        <el-input v-model="userAccount.college" :disabled="true"></el-input>
      </el-form-item>

      <el-form-item label="性别" prop="gender">
        <el-select v-model="userAccount.gender" style="float: left">
          <el-option label="男" value="男"></el-option>
          <el-option label="女" value="女"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="手机" prop="phone">
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
      userAccount: {
        name: "",
        sid: "",
        gender: "",
        phone_number: "",
        email: "",
      },
    };
  },
  methods: {
    save() {
      var jsons = {
        name: this.userAccount.name,
        s_id: this.userAccount.sid,
        gender: this.userAccount.gender,
        phone_number: this.userAccount.phone_number,
        email: this.userAccount.email,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/editInfo/Student/", JSON.stringify(jsons))
        .then((response) => {
          console.log("sava");
          console.log(response);

          if (response.data == "Success") {
            this.$message("修改成功");
            this.getInfo();
          }
        });
    },
    back() {
      this.$router.push("/studentHome/account");
    },
    getInfo() {
      var jsons = {
        s_id: this.userAccount.sid,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/getUserInfo/Student/", JSON.stringify(jsons))
        .then((response) => {
          console.log("getinfo");
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.userAccount.name = response.data["data"][0].name;
            this.userAccount.gender = response.data["data"][0].gender;
            this.userAccount.phone_number =
              response.data["data"][0].phone_number;
            this.userAccount.email = response.data["data"][0].email;
            this.userAccount.is_active = response.data["data"][0].is_active;
            //this.role = response.data[0].role;
            this.userAccount.department = response.data["data"][0].department;
            //this.major_id;
          }
        })
        .catch(function (error) {
          console(error);
        });
    },
  },
  mounted() {
    this.userAccount.sid = sessionStorage.getItem("id");
    this.getInfo();
  },
};
</script>
<style scoped>
.el-button--primary {
  color: white;
}
.el-button--success {
  color: white;
}
</style>

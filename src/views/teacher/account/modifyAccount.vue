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

      <el-form-item label="工号" prop="t_id">
        <el-input v-model="userAccount.t_id" :disabled="true"></el-input>
      </el-form-item>

      <el-form-item label="性别" prop="gender">
        <el-select v-model="userAccount.gender" style="float: left">
          <el-option label="男" :value="'男'"></el-option>
          <el-option label="女" :value="'女'"></el-option>
        </el-select>
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
      userAccount: {},
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    save() {
      if (this.userAccount.phone_number.length != 11) {
        this.$message.warning("请输入11位的手机号！");
        return;
      }

      var jsons = {
        name: this.userAccount.name,
        t_id: this.userAccount.t_id,
        gender: this.userAccount.gender,
        phone_number: this.userAccount.phone_number,
        email: this.userAccount.email,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/editInfo/Teacher/", JSON.stringify(jsons))
        .then((response) => {
          console.log("save");
          console.log(response);

          if (response.data == "Success")
            this.$message({
              message: "修改成功",
              type: "success",
            });
          else this.$message.error("错误");
          this.getTeaInfo();
        });
    },
    back() {
      this.$router.push("/teacherHome/account");
    },
    getTeaInfo() {
      this.axios
        .get("api//getUserInfo/Teacher/", {
          params: { t_id: this.id, token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("老师信息");
          console.log(response);

          this.userAccount = response.data[0];
        })
        .catch(function (error) {
          console(error);
        });
    },
  },
  mounted() {
    this.getParams();
    this.getTeaInfo();
  },
};
</script>
<style >
.el-button--primary {
  color: white;
}
</style>
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
          <el-option label="男" :value="1"></el-option>
          <el-option label="女" :value="0"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="手机" prop="phone">
        <el-input v-model="userAccount.phone"></el-input>
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
        sid: 111,
        gender: "女",
        phone: 111,
        email: "",
      },
    };
  },
  methods: {
    save() {},
    back() {
      this.$router.push("/adminHome/account");
    },
  },
};
</script>

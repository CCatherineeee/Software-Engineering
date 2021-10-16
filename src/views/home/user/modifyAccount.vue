<template>
  <el-row>
    <el-col :span="24">
      <div class="grid-content bg-purple-dark">
        <el-form
          ref="form"
          :model="userAccount"
          label-width="80px"
          v-loading="loading"
        >
          <el-form-item label="学号" prop="userID">
            <el-input v-model="userAccount.userID"></el-input>
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

          <el-form-item label="邮箱" prop="mail">
            <el-input v-model="userAccount.mail"></el-input>
          </el-form-item>

          <el-form-item label="简介" prop="introduction">
            <el-input
              type="textarea"
              v-model="userAccount.introduction"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-button style="margin-left: 80px" type="primary" @click="save"
              >保存修改</el-button
            >
            <el-button style="margin-left: 100px" @click="back">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-col>
  </el-row>
</template>

<script>
export default {
  data() {
    return {
      userAccount: {
        userID: "",
        gender: "女",
        phone: 11111111111,
        mail: "",
        introduction: "",
      },
    };
  },
  methods: {
    back() {
      this.$router.push("/home/user/account");
    },
  },
};
</script>

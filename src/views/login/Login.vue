<template>
  <div style="margin: auto auto; background: rgba(27, 41, 58, 0.85)">
    <el-container class="loginPage">
      <el-main><img src="@/assets/logo.png" /> </el-main>

      <el-aside width="500px" class="loginForm">
        <el-container>
          <el-header height="150px"
            ><p
              style="
                margin: 70px auto 50px auto;
                color: white;
                font: 32px Microsoft YaHei;
              "
            >
              实验教学系统
            </p></el-header
          >
          <el-main>
            <el-form
              ref="ruleForm"
              :model="ruleForm"
              status-icon
              :rules="rules"
              label-width="80px"
            >
              <el-form-item label="用户名" prop="userID" style="padding: auto">
                <el-input
                  v-model="ruleForm.userID"
                  type="text"
                  autocomplete="off"
                  placeholder="请输入邮箱"
                ></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input
                  v-model="ruleForm.password"
                  type="password"
                  autocomplete="off"
                  placeholder="请输入密码"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="text">忘记密码</el-button>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="submitForm(ruleForm)"
                  style="margin-right: 50px"
                  >登陆</el-button
                >
                <el-button @click="toRegister" style="margin-left: 50px"
                  >注册</el-button
                >
              </el-form-item>
            </el-form>
          </el-main>
        </el-container>
      </el-aside>
    </el-container>
  </div>
</template>

<script>
//import axios from "axios";

export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入邮箱"));
      } else {
        if (this.ruleForm.userID !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    const validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        userID: "",
        password: "",
      },
      rules: {
        userID: [{ validator: validatePass, trigger: "blur" }],
        password: [{ validator: validatePass2, trigger: "blur" }],
      },
    };
  },
  methods: {
    submitForm() {
      if (this.ruleForm.userID === "" && this.ruleForm.password === "") {
        this.$message("账户和密码不能为空！");
      } else if (this.ruleForm.userID === "") {
        this.$message("请输入账户！");
      } else if (this.ruleForm.password === "") {
        this.$message("请输入密码！");
      } else {
        //this.axios.defaults.baseURL = 'http://127.0.0.1:5000/'
        this.axios({
          methods: "GET",
          // baseURL:'http://127.0.0.1:5000/',
          url: "/api/get/",
          changeOrigin: true, // 是否跨域
          data: JSON.stringify({
            //这里是发送给后台的数据
            userID: this.ruleForm.userID,
            password: this.ruleForm.password,
          }),
        }).then((response) => {
          //这里使用了ES6的语法
          console.log(response); //请求成功返回的数据
        });
        console.log();
      }
    },
    toRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style>
body > .el-container {
  margin-bottom: 40px;
}

.loginPage {
  text-align: center;
  background: #dfd3d3;
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 570px;
}

.loginForm {
  background: rgba(27, 41, 58, 0.85);
  color: var(--el-text-color-primary);
  text-align: center;
  line-height: 570px;
}
</style>
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
              管理员登录
            </p></el-header
          >
          <el-main>
            <el-form
              ref="loginForm"
              :model="ruleForm"
              status-icon
              :rules="rules"
              label-width="80px"
            >
              <el-form-item label="用户名" prop="userID" style="padding: auto">
                <el-input
                  v-model="ruleForm.username"
                  type="text"
                  autocomplete="off"
                  placeholder="请输入用户名"
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
                <el-button
                  type="primary"
                  @click="submitForm()"
                  style="margin-right: 50px"
                  >登陆</el-button
                >
                <el-button @click="toRegister" style="margin-left: 50px"
                  >注册</el-button
                >
              </el-form-item>
              <el-form-item>
                <el-row :gutter="2">
                  <el-col :span="12"
                    ><t class="text-button">忘记密码</t></el-col
                  >
                  <el-col :span="12"
                    ><t class="text-button" @click="Login()"
                      >用户登录</t
                    ></el-col
                  >
                </el-row>
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
    const validateName = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入用户名"));
      } else {
        if (this.ruleForm.userID !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        callback();
      }
    };
    return {
      ruleForm: {
        username: "",
        password: "",
      },
      rules: {
        userName: [{ validator: validateName, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
      },
    };
  },
  methods: {
    Login() {
      this.$router.push("/Login");
    },
    submitForm() {
      if (this.ruleForm.userName === "" && this.ruleForm.password === "") {
        this.$message("账户和密码不能为空！");
      } else if (this.ruleForm.Name === "") {
        this.$message("请输入用户名！");
      } else if (this.ruleForm.password === "") {
        this.$message("请输入密码！");
      } else {
        this.axios
          .post(
            "/api/adminLogin/",
            JSON.stringify({
              username: this.ruleForm.username,
              password: this.ruleForm.password,
            })
          )
          .then((response) => {
            console.log(response.data.status);
            if (response.data.status === "UserNotExist") {
              this.$message("用户不存在");
            } else if (response.data.status === "PasswordWrong") {
              this.$message("密码错误！");
            }
            if (response.data.status === "Login") {
              this.$message("登录成功！");
              sessionStorage.setItem("id", this.ruleForm.username);
              sessionStorage.setItem("token", response.data.token);
              this.$router.push("/adminHome");
              this.$router.push("/adminHome");
            }
          })
          .catch((error) => {
            this.$message("网络错误！");
            console.log(error);
          });
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
  background: #ffffff;
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
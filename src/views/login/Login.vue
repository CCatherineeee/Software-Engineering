<template>
  <div style="margin: auto auto">
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
              <el-form-item label="用户名" prop="userID">
                <el-input
                  v-model="ruleForm.userID"
                  type="text"
                  autocomplete="off"
                  placeholder="请输入学号"
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
                  @click="submitForm(ruleForm)"
                  style="margin-right: 50px"
                  >登陆</el-button
                >
                <el-button @click="toRegister" style="margin-left: 50px"
                  >注册</el-button
                >
                <br />
                <br />
                <el-form-item>
                  <el-row :gutter="2">
                    <el-col :span="8"
                      ><t class="text-button">忘记密码</t></el-col
                    >
                    <el-col :span="8"
                      ><t class="text-button">教师登录</t></el-col
                    >
                    <el-col :span="8"
                      ><t class="text-button" @click="AdminLogin()"
                        >管理员登录</t
                      ></el-col
                    >
                  </el-row>
                </el-form-item>
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
        callback(new Error("请输入学号"));
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
    AdminLogin() {
      this.$router.push("/AdminLogin");
    },
    submitForm() {
      if (this.ruleForm.userID === "" && this.ruleForm.password === "") {
        this.$message("账户和密码不能为空！");
      } else if (this.ruleForm.userID === "") {
        this.$message("请输入账户！");
      } else if (this.ruleForm.password === "") {
        this.$message("请输入密码！");
      } else {
        let config = {
          headers: { "Content-Type": "multipart/form-data" },
        };
        this.axios
          .post(
            "/api/login/",
            {
              params: {
                releForm: this.releForm,
              },
            },
            config
          )
          .then((response) => {
            //这里使用了ES6的语法
            console.log(response); //请求成功返回的数据
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
  line-height: 570px;
}

.loginForm {
  text-align: center;
  line-height: 570px;
}
.text-button {
  color: white;
}
.text-button:hover {
  color: #bbdefb;
}
</style>
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
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="text">忘记密码</el-button>
              </el-form-item>
              <el-form-item>
                <el-button
                  type="primary"
                  @click="submitForm(formName)"
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

<script lang="ts">
//import axios from "axios";

export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入用户名"));
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
      /*var that = this;
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const path = "http://127.0.0.1:5000/login";
      axios.get(path).then(function (response) {
        // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
        // 可以直接通过 response.data 取key-value
        // 坑一：这里不能直接使用 this 指针，不然找不到对象
        var msg = response.data.msg;
        // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
        that.serverResponse = msg;

        alert("Success " + response.status + ", " + response.data + ", " + msg);
      });*/
      /*this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("登录成功!");
        } else {
          console.log("登录失败!!");
          return false;
        }
      });*/
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
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
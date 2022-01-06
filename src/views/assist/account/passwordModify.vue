<template>
   <el-container style="margin-top:20px;">
    <el-main>
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
          :model="form"
          label-width="80px"
        >
          <el-form-item label="新密码" :required="true" status-icon="true">
            <el-input type="password" v-model="form.password"></el-input>
          </el-form-item>

          <el-form-item label="再次输入" :required="true" status-icon="true">
            <el-input type="password" v-model="form.passwordC"></el-input>
          </el-form-item>

          <el-form-item
            label="邮箱"
            :required="true"
            prop="email"
            status-icon="true"
          >
            <el-input v-model="form.email"></el-input
            ><el-button type="text" @click="sendCaptcha">发送验证码</el-button>
          </el-form-item>

          <el-form-item>
            <el-button style="margin-left: 30%" @click="save()" type="primary"
              >确认修改</el-button
            >
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        password: "",
        passwordC: "",
      },
    };
  },
  methods: {
    save() {},
    back() {
      this.$router.push("/teacherHome");
    },
        sendCaptcha() {
      console.log(this.email);
      this.axios
        .post(
          //"/api/users/sendCaptcha"
          "/api/users/sendCaptcha",
          JSON.stringify({
            email: this.email,
          })
        )
        .then(
          function (response) {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            alert("发送验证码成功");
            console.log(response);
          },
          function (err) {
            console.log(err);
          }
        );
    },
  },
};
</script>

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
          <el-form-item label="原密码" :required="true" status-icon="true">
            <el-input type="password" v-model="form.oripassword"></el-input>
          </el-form-item>

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
            <el-input v-model="form.email"></el-input>
          </el-form-item>

          <el-form-item label="验证码" :required="true" status-icon="true">
            <el-input type="text" v-model="form.captcha"></el-input>
          </el-form-item>

          <el-form-item  :required="true" status-icon="true">
            <el-button type="text" @click="sendCaptcha">发送验证码</el-button>
          </el-form-item>

          <el-form-item>
            <el-button style="margin-left: 30%" @click="validateCaptcha()" type="primary"
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
        oripassword:"",
        captcha:"",
        captchaSuccess:"false",
      },
    };
  },
  methods: {
      validateCaptcha(){
        this.form.captchaSuccess = "false";
        var result = [];
        this.axios
            .post(
              //"/api/users/validateCaptcha"
              "/api/users/validateCaptcha",
              JSON.stringify({
                email: this.form.email,
                captcha: this.form.captcha
              })
            )
            .then(function(response) {
              //这里使用了ES6的语法
              // this.checkResponse(response.data); //请求成功返回的数据
              result = response.data.message
              console.log(result)
            // if (result == "true")
            // {this.captchaSuccess="ture";}

            },function(err){
              console.log(err)
            });
          // if (result == "true")
          //   {commitJson.verifySuccess=="ture";}
          setTimeout(()=>{
             if (result == "true")
            {this.form.captchaSuccess="true";}
            this.save(this.form.captchaSuccess,this.form.oripassword,this.form.password)
          },2500)
      },
    save(captchaSuccess,old_password,new_password) {

        if(this.password!=this.passwordC)
        {
          //弹出错误提示
          alert("两次密码输入不一样!")
        }
        else{
          if(captchaSuccess=="true"){
            this.axios
              .post(
                //"/api/users/validateCaptcha"
                "/api/editInfo/Student/changePwd",
                JSON.stringify({
                  s_id: sessionStorage.getItem("id"),
                  old_password: old_password,
                  new_password: new_password
                })
              )
              .then(function(response) {
                //这里使用了ES6的语法
                // this.checkResponse(response.data); //请求成功返回的数据
                alert("修改成功");
                this.$router.go(0);
                console.log(response)

              }, function(err){
                console.log(err)
              });
            setTimeout(()=>{
              this.$router.go(0);
          },1500)
            }
            else{
              this.$message("验证码错误")
            }
        }
    },
    back() {
      this.$router.push("/studentHome");
    },
    sendCaptcha() {
      console.log(this.form.email);
      this.axios
        .post(
          //"/api/users/sendCaptcha"
          "/api/users/sendCaptcha",
          JSON.stringify({
            email: this.form.email,
          })
        )
        .then(
          function (response) {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
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

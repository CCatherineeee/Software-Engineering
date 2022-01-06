<template>
  <transition name="bounce">
    <div class="kiko-confirm" v-if="visible">
      <div class="bg"></div>
      <div class="kiko-container" :style="{width: width}">
        <div class="header" >
          {{title}}
          <!-- <i @click="close" class="icon-remove icon-large kiko-close-btn" ></i> -->
        </div>
        <div class="content">
          <slot>
             <el-button class="cancel" plain @click="close">取消</el-button>
             <el-button class="sure" type="primary" plain @click="validateCaptcha"> 确定</el-button>
          </slot>
        </div>
        <slot name="footer">
        </slot>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    name: 'kiko-confirm',
    props: {
      width: {
        type: String,
        default: '260px'
      },
      title: {
        type: String,
        default: '信息'
      },
      visible: {
        type: Boolean,
        default: false
      },
      closeVisible: {
        type: Boolean,
        default: true
      }
    },
    data () {
      return {
        verifySuccess:"false",
      }
    },
    methods: {
      validateCaptcha(){
        var commitJson = this.$store.state.data;
        var result = [];
        this.axios
            .post(
              //"/api/users/validateCaptcha"
              "/api/users/validateCaptcha",
              JSON.stringify({
                email: commitJson.email,
                captcha: commitJson.captcha
              })
            )
            .then(function(response) {
              //这里使用了ES6的语法
              // this.checkResponse(response.data); //请求成功返回的数据
              result = response.data.message
              console.log(result)
            if (result == "true")
            {commitJson.verifySuccess="ture";}

            },function(err){
              console.log(err)
            });
          // if (result == "true")
          //   {commitJson.verifySuccess=="ture";}
          setTimeout(()=>{
            this.sure(commitJson)
          },2000)
          this.visible = false;
          this.$router.push({path:"/Login"});
      },
      sure(commitJson){
        // var commitJson = this.$store.state.data
        
        if(commitJson.newPsw!=commitJson.confirmNewPsw)
        {
          //弹出错误提示
          alert("两次密码输入不一样!")
        }
        else{

        if(commitJson.role=="student" && commitJson.verifySuccess=="ture"){
            this.axios
            .post(
              //"/api/users/validateCaptcha"
              "/api/editInfo/Student/resetPwd",
              JSON.stringify({
                s_id: commitJson.id,
                new_password: commitJson.newPsw
              })
            )
            .then(function(response) {
              //这里使用了ES6的语法
              // this.checkResponse(response.data); //请求成功返回的数据
              alert("重置学生密码成功");
              console.log(response)

            }, function(err){
              console.log(err)
            });
              }
        else if(commitJson.role=="teacher" && commitJson.verifySuccess=="ture"){
            this.axios
            .post(
              //"/api/users/validateCaptcha"
              "/api/editInfo/Teacher/resetPwd",
              JSON.stringify({
                t_id: commitJson.id,
                new_password: commitJson.newPsw
              })
            )
            .then(function(response) {
              //这里使用了ES6的语法
              // this.checkResponse(response.data); //请求成功返回的数据
              alert("重置教师密码成功");
              console.log(response)

            }, function(err){
              console.log(err)
            });
              }
        else if(commitJson.role=="teachingAssistant" && commitJson.verifySuccess=="ture"){
              alert("助教还没写");

              }
        else{
          alert("验证码错误");
          this.visible = false;
          return
        }
      }
      },
      close () {
        this.visible = false;
      }
    }
  }
</script>

<style type="text/css">
  .bounce-enter-active {
   -webkit-transform: scale(2);
    -moz-transform: scale(2);
    -ms-transform: scale(2);
    transform: scale(2);
    opacity: 0;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
  }
  .bounce-leave-active {
    -webkit-transform: scale(2);
    -moz-transform: scale(2);
    -ms-transform: scale(2);
    transform: scale(2);
    opacity: 0;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
  }
  /* [@keyframes](/user/keyframes) bounce-in {
    -webkit-transform: scale(2);
    -moz-transform: scale(2);
    -ms-transform: scale(2);
    transform: scale(2);
    opacity: 0;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;} */
  .kiko-confirm {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999999;
  }
  .kiko-confirm .bg {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    /*background-color: #FFFFFF;*/
    background-color: #000;
    opacity: 0.3;
    z-index: 99999;
  }
  .kiko-confirm .kiko-container {
    position: absolute;
    display: inline-block;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 260px;
    min-width: 260px;
    z-index: 9999999999999;
  }
  .kiko-confirm .kiko-container .header {
    width: 100%;
    padding: 10px;
    background-color: #fff;
    border-bottom: 1px solid #eee;
    color: #000;
    text-align: center;
  }
  .kiko-confirm .kiko-container .content {
    width: 100%;
    padding: 10px;
    background-color: #FFFFFF;
  }
  .kiko-confirm .kiko-container .kiko-footer {
    width: 100%;
    padding: 10px;
    background-color: #FFFFFF;
    text-align: right;
    border-top: 1px solid #eee;
  }
  .kiko-btn {
    padding: 5px 15px;
    text-decoration: none !important;
    border-radius: 2px;
    margin: 6px 6px 0 6px;
  }
  .kiko-btn:hover {
    text-decoration:  none !important;
  }
  .kiko-btn:active {
    text-decoration:  none !important;
  }
  .kiko-btn.make-sure {
    background-color: #4575A6;
    color: #fff;
  }
  .kiko-btn.cancel {
    background-color: #BBB5B5;
    color: #fff;
  }
  .kiko-close-btn {
    cursor: pointer;
    float: right;
  }
</style>

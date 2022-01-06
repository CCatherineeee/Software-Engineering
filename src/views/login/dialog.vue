<template>
  <div class="dialog" id="dialog" v-show="showMask">
    <div class="dialog-container">
      <div class="dialog-title">重置密码</div>
      <!-- <div class="content" v-html="content"></div> -->

      <el-form style="margin: 40px 100px 0px 50px" label-width="80px">
        <el-form-item label="您的身份">
          <el-radio v-model="role" label="student">学生</el-radio>
          <el-radio v-model="role" label="teacher">老师</el-radio>
          <el-radio v-model="role" label="teachingAssistant">助教</el-radio>
        </el-form-item>
        <el-form-item label="学工号" :required="true" status-icon="true">
          <el-input v-model="id"></el-input>
        </el-form-item>
        <el-form-item label="新密码" :required="true" status-icon="true">
          <el-input type="password" v-model="newPsw"></el-input>
        </el-form-item>

        <el-form-item label="再次输入" :required="true" status-icon="true">
          <el-input type="password" v-model="confirmNewPsw"></el-input>
        </el-form-item>

        <el-form-item label="邮箱" :required="true" status-icon="true">
          <el-input v-model="email"></el-input>
        </el-form-item>

        <el-form-item label="验证码" :required="true" status-icon="true">
          <el-input v-model="captcha"></el-input>
        </el-form-item>
        <el-button type="text" @click="sendCaptcha">发送验证码</el-button>
      </el-form>
      <div class="btns">
        <div v-if="type != 'confirm'" class="default-btn" @click="closeBtn">
          退出
        </div>
        <div v-if="type == 'danger'" class="danger-btn" @click="dangerBtn">
          提交
        </div>
        <!-- <myconfirm title="确认重置?"  ref="confirmChange">
        </myconfirm>
         -->
      </div>

      <div class="close-btn" @click="closeMask">
        <i class="iconfont icon-close"></i>
      </div>
    </div>
    <div>
      <myconfirm title="确认重置?" ref="confirmChange"> </myconfirm>
    </div>
  </div>
</template>
<script>
import confirm from "./confirm.vue";

export default {
  components: {
    myconfirm: confirm,
  },
  props: {
    value: {},
    // 类型包括 defalut 默认， danger 危险， confirm 确认，
    type: {
      type: String,
      default: "default",
    },
    content: {
      type: String,
      default: "",
    },
    title: {
      type: String,
      default: "",
    },
    cancelText: {
      type: String,
      default: "退出",
    },
    dangerText: {
      type: String,
      default: "提交",
    },
  },
  data() {
    return {
      showMask: false,
      id: "",
      newPsw: "",
      confirmNewPsw: "",
      email: "",
      captcha: "",
      role: "student",
    };
  },
  methods: {
    destroyed() {
      var vm = this;
      vm._isDestroyed = true
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
            // alert("发送验证码成功");
            console.log(response);
          },
          function (err) {
            console.log(err);
          }
        );
    },
    closeMask() {
      this.showMask = false;
    },
    closeBtn() {
      this.$emit("cancel");
      this.closeMask();
      this.id="";
      this.newPsw= "";
      this.confirmNewPsw= "";
      this.email= "";
      this.captcha="";
      this.role= "student";
    },
    //在这里修改
    dangerBtn() {
      this.$emit("danger");

      this.$store.state.data = {
        id: this.id,
        role: this.role,
        newPsw: this.newPsw,
        confirmNewPsw: this.confirmNewPsw,
        email: this.email,
        captcha: this.captcha,
        verifySuccess: false,
      };
      console.log("this.$store.state.data", this.$store.state.data);
      this.$refs.confirmChange.visible = true;
      // this.closeMask();
    },
    confirmBtn() {
      this.$emit("confirm");
      this.closeMask();
    },
  },
  mounted() {
    this.showMask = this.value;
    this.id="";
    this.newPsw= "";
    this.confirmNewPsw= "";
    this.email= "";
    this.captcha="";
    this.role= "student";
  },
  watch: {
    value(newVal) {
      this.showMask = newVal;
    },
    showMask(val) {
      this.$emit("input", val);
    },
  },
};
</script>
<style lang="less" scoped>
.dialog {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 9999;
  .dialog-container {
    width: 500px;
    height: 460px;
    background: #ffffff;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 8px;
    position: relative;
    .dialog-title {
      width: 100%;
      height: 60px;
      font-size: 18px;
      color: #696969;
      font-weight: 600;
      padding: 16px 50px 0 20px;
      box-sizing: border-box;
    }
    .content {
      color: #797979;
      line-height: 26px;
      padding: 0 20px;
      box-sizing: border-box;
    }
    .inp {
      margin: 10px 0 0 20px;
      width: 200px;
      height: 40px;
      padding-left: 4px;
      border-radius: 4px;
      border: none;
      background: #efefef;
      outline: none;
      &:focus {
        border: 1px solid #509ee3;
      }
    }
    .btns {
      width: 100%;
      height: 60px;
      // line-height: 60px;
      position: absolute;
      bottom: 0;
      left: 0;
      text-align: right;
      padding: 0 16px;
      box-sizing: border-box;
      & > div {
        display: inline-block;
        height: 40px;
        line-height: 40px;
        padding: 0 14px;
        color: #ffffff;
        background: #f1f1f1;
        border-radius: 8px;
        margin-right: 12px;
        cursor: pointer;
      }
      .default-btn {
        color: #787878;
        &:hover {
          color: #509ee3;
        }
      }
      .danger-btn {
        background: #ef8c8c;
        &:hover {
          background: rgb(224, 135, 135);
        }
        &:active {
          background: #ef8c8c;
        }
      }
      .confirm-btn {
        color: #ffffff;
        background: #509ee3;
        &:hover {
          background: #6fb0eb;
        }
      }
    }
    .close-btn {
      position: absolute;
      top: 16px;
      right: 16px;
      width: 30px;
      height: 30px;
      line-height: 30px;
      text-align: center;
      font-size: 18px;
      cursor: pointer;
      &:hover {
        font-weight: 600;
      }
    }
  }
}
</style>

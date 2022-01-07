<template>
  <div style="height: 800px; background: #e6cfcc">
    <el-container>
      <el-main>
        <div
          style="
            width: 600px;
            height: 700px;
            margin: 30px auto;
            background: rgba(27, 41, 58, 0.85);
            box-shadow: 5px 5px 10px;
          "
        >
          <p
            style="
              margin: 40px 0px 0px 0px;
              padding-top: 20px;
              color: white;
              font: 32px Microsoft YaHei;
              text-align: center;
            "
          >
            激活账号
          </p>
          <el-form
            style="margin: 40px 65px 0px 25px"
            ref="form"
            :model="form"
            label-width="80px"
          >
            <el-form-item
              label="姓名"
              :rules="nameRules"
              prop="name"
              status-icon="true"
            >
              <el-input v-model="form.name"></el-input>
            </el-form-item>

            <el-form-item
              label="学号"
              :rules="sidRules"
              prop="sid"
              status-icon="true"
            >
              <el-input v-model="form.sid"></el-input>
            </el-form-item>

            <el-form-item label="密码" :required="true" status-icon="true">
              <el-input type="password" v-model="form.password"></el-input>
            </el-form-item>

            <el-form-item label="邮件" style="color: white" :required="true">
              <el-input v-model="form.phone"></el-input>
            </el-form-item>

            <el-form-item style="text-align: center">
              <el-button type="primary" @click="submitLoginForm()"
                >激活</el-button
              >
              <el-button style="margin-left: 100px" @click="back"
                >返回</el-button
              >
            </el-form-item>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        name: "",
        password: "",
        passwordC: "",
        college: "",
        phone: "",
      },
      options: [
        {
          value: "软件学院",
          label: "软件学院",
        },
        {
          value: "电信学院",
          label: "电信学院",
        },
        {
          value: "汽车学院",
          label: "汽车学院",
        },
        {
          value: "土木学院",
          label: "土木学院",
        },
        {
          value: "经管学院",
          label: "经管学院",
        },
        {
          value: "材料学院",
          label: "材料学院",
        },
        {
          value: "数学学院",
          label: "数学学院",
        },
        {
          value: "物理学院",
          label: "物理学院",
        },
        {
          value: "化学学院",
          label: "化学学院",
        },
      ],
      nameRules: [{ required: true, message: "请输入姓名", trigger: "blur" }],
      sidRules: [
        {
          type: "number",
          required: true,
          message: "请输入学号",
          trigger: "blur",
        },
      ],
    };
  },
  methods: {
    submitForm() {
      console.log(JSON.stringify(this.form));

      this.axios
        .post("/api/register/", JSON.stringify(this.form))
        .then((response) => {
          //这里使用了ES6的语法
          console.log(response); //请求成功返回的数据
        });
    },
    back() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
#loginMain {
  background: rgba(229, 204, 200, 0.56);
  /*#9c0406*/
  height: 100%;
  width: 100%;
  margin: 0 auto;
}
</style>
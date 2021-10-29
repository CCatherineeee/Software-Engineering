<template>
  <el-container>
    <el-aside></el-aside>
    <el-main>
      <el-card>
        <table class="demo-border">
          <tbody
            style="
              margin: 40px 0px 0px 0px;
              padding-top: 20px;
              color: black;
              font: 18px;
              text-align: center;
            "
          >
            <tr>
              <p>学号 ：</p>
              <td>{{ userID }}</td>
            </tr>
            <tr>
              <p>姓名 ：</p>
              <td>{{ name }}</td>
            </tr>
            <tr>
              <p>学院 ：</p>
              <td>{{ colleague }}</td>
            </tr>
            <tr>
              <p>邮箱 ：</p>
              <td>{{ email }}</td>
            </tr>
            <tr>
              <p>手机 ：</p>
              <td>{{ phone }}</td>
            </tr>
            <tr>
              <p>性别 ：</p>
              <td>{{ gender }}</td>
            </tr>
            <tr>
              <p></p>
            </tr>
            <tr>
              <el-button @click="modifyAccount" type="primary"
                >修改个人资料</el-button
              >
            </tr>
          </tbody>
        </table>
      </el-card>
    </el-main>
    <el-aside></el-aside>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      userID: 1951104,
      name: "xzq",
      colleague: "",
      email: "1442391739@qq.com",
      phone: 10086,
      gender: "女",
    };
  },
  methods: {
    modifyAccount() {
      this.$router.push("/home/user/modifyAccount");
    },
  },
};
</script>


<style scoped>
.demo-border .text {
  width: 15%;
}

.demo-border .line div {
  width: 100%;
  height: 0;
}
</style>

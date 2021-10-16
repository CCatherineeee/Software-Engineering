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
              color: white;
              font: 32px Microsoft YaHei;
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
              <td>{{ mail }}</td>
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
      mail: "1442391739@qq.com",
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

<!-- 个人信息页面-->
<template>
  <el-container style="margin-top: 20px">
    <el-aside width="200px"></el-aside>
    <el-main class="back">
      <el-card style="box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15)">
        <el-descriptions
          title="账户信息"
          :column="2"
          border
          size="medium"
          box-shadow="15px 15px 10px"
        >
          <template slot="extra">
            <el-button type="primary" size="medium" @click="modifyAccount()"
              >编辑</el-button
            >
          </template>
          <el-descriptions-item>
            <template slot="label"> 姓名 </template>
            {{ name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 工号 </template>
            {{ id }}
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"> 手机号 </template>
            {{ phone_number }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 邮箱 </template>
            {{ email }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-main>
    <el-aside width="200px"></el-aside>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      name: "",
      id: "",
      phone_number: "",
      email: "",
      is_active: "",
      //role: "",
      department: "",
      major_id: "",
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数

      this.id = sessionStorage.getItem("id");
    },

    getAdminInfo() {
      this.axios
        .get("/api/getAdminInfo/admin/", {
          params: { admin_id: this.id, token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getAdminInfo", response);
          this.name = response.data[0].name;
          //this.gender = response.data[0].gender;
          this.phone_number = response.data[0].phone_number;
          this.email = response.data[0].email;
          //this.is_active = response.data[0].is_active;
          //this.role = response.data[0].role;
          //this.department = response.data[0].department;
          //this.major_id;
        })
        .catch((error) => {
          this.$message("网络错误！");
          console.log(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/adminHome/modifyAccount",
        query: {
          info: this.$Base64.encode(JSON.stringify(this.id)),
        },
      });
    },
  },
  mounted() {
    this.getParams();
    this.getAdminInfo();
  },
};
</script>


<style scoped>
.back {
  width: 700px;
}
.demo-border .text {
  width: 15%;
}

.demo-border .line div {
  width: 100%;
  height: 0;
}
.el-button--primary {
  color: white;
}
</style>

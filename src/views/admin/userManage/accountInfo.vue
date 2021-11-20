<!-- 个人信息页面-->
<template>
  <el-container>
    <el-main>
      <el-card>
        <el-descriptions title="账户信息" :column="2" border size="medium">
          <template slot="extra">
            <el-button type="primary" size="medium" @click="back"
              >返回</el-button
            >
            <el-button type="primary" size="medium" @click="modifyAccount()"
              >编辑</el-button
            >
          </template>
          <el-descriptions-item>
            <template slot="label"> 姓名 </template>
            {{ name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 学号 </template>
            {{ id }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 性别 </template>
            {{ gender }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 手机号 </template>
            {{ phone_number }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 邮箱 </template>
            {{ email }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 状态 </template>
            <el-tag
              :type="is_active === 1 ? 'success' : 'danger'"
              disable-transitions
              ><span v-if="is_active === 1">激活</span>
              <span v-if="is_active === 0">非激活</span></el-tag
            >
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"> 学院 </template>
            {{ department }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 专业 </template>
            {{ major_id }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-main>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      name: "",
      id: "",
      gender: "",
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
      var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内
      console.log("传来的参数==" + routerParams);
      this.id = routerParams;
    },

    getStuInfo() {
      this.axios
        .get("/api/getUserInfo/Student/", {
          params: { s_id: this.id },
          crossDomain: true,
        })
        .then((response) => {
          console.log(response.data);
          this.name = response.data[0].name;
          this.gender = response.data[0].gender;
          this.phone_number = response.data[0].phone_number;
          this.email = response.data[0].email;
          this.is_active = response.data[0].is_active;
          //this.role = response.data[0].role;
          this.department = response.data[0].department;
          //this.major_id;
        })
        .catch(function (error) {
          console(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/adminHome/userManage/accountModify",
        query: { id: this.id },
      });
    },
    back() {
      this.$router.push("/adminHome/userManage/accountCheck");
    },
  },
  mounted() {
    this.getParams();
    this.getStuInfo();
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

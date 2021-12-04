<!-- 个人信息页面-->
<template>
  <el-container>
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
    <el-aside width="200px"></el-aside>
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

      this.id = sessionStorage.getItem('id');
    },

    getStuInfo() {
      this.axios
        .post("/api/getUserInfo/Student/",
          JSON.stringify({ s_id: this.id ,token:sessionStorage.getItem('token')}))
        .then((response) => {
          console.log(response.data['data']);
          if(response.data['code'] === 301) {
            this.$message("验证过期")
            this.$router.push({path:"/login"})
          }
          else if(response.data['code'] === 404) {
            this.$message("找不到页面")
            this.$router.push({path:"/404"})
          }
          else {

            this.name = response.data['data'][0].name;
            this.gender = response.data['data'][0].gender;
            this.phone_number = response.data['data'][0].phone_number;
            this.email = response.data['data'][0].email;
            this.is_active = response.data['data'][0].is_active;
            //this.role = response.data[0].role;
            this.department = response.data['data'][0].department;
            //this.major_id;
          }
        })
        .catch(function (error) {
          console(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/studentHome/modifyAccount"});
    },
  },
  mounted() {
    this.getParams();
    this.getStuInfo();
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
</style>

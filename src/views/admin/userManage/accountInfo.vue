<!-- 个人信息页面-->
<template>
  <el-container style="margin-top: 20px">
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
      department: "",
      major_id: "",
      role: "",
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      //var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内

      this.id = JSON.parse(this.$Base64.decode(this.$route.query.info))["id"];
      this.role = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "role"
      ];
      console.log("路有参数" + this.id + this.role);
    },

    getInfo() {
      if (this.role == 1) {
        var jsons = {
          s_id: this.id,
        };
        this.axios
          .post("/api/getUserInfo/Student/", JSON.stringify(jsons))
          .then((response) => {
            console.log("getInfo", response);
            this.name = response.data.data[0].name;
            this.gender = response.data.data[0].gender;
            this.phone_number = response.data.data[0].phone_number;
            this.email = response.data.data[0].email;
            this.is_active = response.data.data[0].is_active;
            //this.role = response.data[0].role;
            this.department = response.data.data[0].department;
            //this.major_id;
          })
          .catch(function (error) {
            console.log(error);
          });
      } else if (this.role == 2) {
        /*var json = {
          t_id: this.id,
        };*/
        this.axios
          .get("/api/getUserInfo/Teacher/", {
            params: {
              t_id: this.id,
            },
          })
          .then((response) => {
            console.log("getInfo");
            console.log(response);
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
            console.log(error);
          });
      } else if (this.role == 3) {
        /* var jso = {
          ta_id: this.id,
        };*/
        this.axios
          .get("/api/getUserInfo/TA/", {
            params: {
              ta_id: this.id,
            },
          })
          .then((response) => {
            console.log("getInfo");
            console.log(response);

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
            console.log(error);
          });
      }
    },

    modifyAccount() {
      this.$router.push({
        path: "/adminHome/userManage/accountModify",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ id: this.id, role: this.role })
          ),
        },
      });
    },
    back() {
      this.$router.go(-1);
    },
  },
  mounted() {
    this.getParams();
    this.getInfo();
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

.el-button--primary {
  color: white;
}
</style>

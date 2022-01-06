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
            <template slot="label"> 学号 </template>
            {{ id }}
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
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },

    getTaInfo() {
      this.axios
        .get("/api/getUserInfo/TA/", {
          params: { ta_id: this.id },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getTaInfo", response);

          this.name = response.data[0].name;

          this.email = response.data[0].email;
          this.is_active = response.data[0].is_active;
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/assistHome/modifyAccount",
      });
    },
  },
  mounted() {
    this.getParams();
    this.getTaInfo();
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

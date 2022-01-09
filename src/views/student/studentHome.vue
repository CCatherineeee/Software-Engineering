<template>
  <div>
    <el-container class="back">
      <el-aside width="15%">
        <div>
          <el-menu class="admin-aside-menu" router>
            <img ref="stuAvatar" class="admin-aside-menu-head" />
            <el-menu-item index="/studentHome/control">
              <i class="el-icon-reading"></i>
              <span slot="title">控制面板</span>
            </el-menu-item>
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-edit"></i>
                <span>个人信息</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/studentHome/account"
                  >查看个人资料</el-menu-item
                >
                <el-menu-item index="/studentHome/modifyPassword"
                  >修改密码</el-menu-item
                >
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="/studentHome/course">
              <i class="el-icon-user"></i>
              <span slot="title">我的课程</span>
            </el-menu-item>
            <el-menu-item index="/studentHome/accounce">
              <i class="el-icon-reading"></i>
              <span slot="title">系统公告</span>
            </el-menu-item>
            <el-menu-item index="/" @click="Logout()">
              <i class="el-icon-reading"></i>
              <span slot="title">退出登录</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      <el-main style="height: 900px">
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      avartar: "<div style='background:#666666'></div>",
    };
  },
  methods: {
    Logout() {
      sessionStorage.removeItem("role");
      sessionStorage.removeItem("id");
      sessionStorage.removeItem("token");
    },
    getUserAvatar: function () {
      let param = new FormData(); // 创建form对象
      param.append("s_id", sessionStorage.getItem("id"));
      this.axios
        .post("/api/getUserInfo/Student/showAvatar", param)
        .then((response) => {
          var address = "http://39.107.51.181:5000";
          var url = response.data.url;
          this.$refs.stuAvatar.src = address + url;
          console.log(this.$refs.stuAvatar.src);
          // var imgHtml = "<img src=" + address + url + "></img>";
          // console.log(imgHtml);

          // this.avatar = imgHtml;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
  },
  mounted() {
    this.getUserAvatar();
  },
};
</script>

<style scoped>
.el-main {
  background-color: #ffffff;
  color: #333;
  text-align: left;
  height: 650px;
  border-radius: 20px;
}
.back {
  margin-left: 10px;
  margin-top: 20px;
}
.admin-aside-menu {
  box-shadow: 3px 3px 10px #d3d3d3;
  background: #f0f8ff;
  border-radius: 10%;
  height: 800px;
  margin-top: 20px;
}
.admin-aside-menu-head {
  margin: 20px auto;
  width: 70%;
  height: 150px;
  border-radius: 50%;
}
</style>

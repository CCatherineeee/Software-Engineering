<template>
  <div>
    <el-container class="back">
      <el-aside width="15%">
        <div>
          <el-menu class="admin-aside-menu" router>
            <img
              src="https://www.w3school.com.cn/i/photo/coffee.jpg"
              class="admin-aside-menu-head"
            />
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
          </el-menu>
        </div>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data(){
    return{
    avartar:"<div style='background:#666666'></div>",
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
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
  margin-top:20px;
}
.admin-aside-menu {
  box-shadow: 3px 3px 10px #d3d3d3;
  background: #F0F8FF;
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

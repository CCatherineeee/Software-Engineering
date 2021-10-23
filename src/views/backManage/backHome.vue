<template>
<el-row>
  <el-col :span="6">
    <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="1">
            <template slot="title">
              <i class="el-icon-location"></i>
              <span>个人中心</span>
            </template>
          </el-menu-item>

          <el-submenu index="userManage">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span slot="title">用户管理</span>
            </template>
            <el-menu-item >管理已有用户</el-menu-item>
            <el-menu-item @click="toAddUser">新增用户用户</el-menu-item>
          </el-submenu>

          <el-menu-item index="4">
            <i class="el-icon-setting"></i>
            <span slot="title">导航四</span>
          </el-menu-item>
    </el-menu>
  </el-col>
     <transition name="slide-fade">
      <!--路由占位符-->
      <router-view></router-view>
      </transition>
</el-row>
</template>

<script>
  export default {
    methods: {
      handleOpen() {

      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
      toAddUser(){
        this.$router.push('/addUser');
      }
    }
  }
</script>

<style scoped>
.el-aside {
  background-color: #545c64;
  color: #333;
  text-align: center;
  line-height: 650px;
}

.el-main {
  background-color: #e1e1e1;
  color: #333;
  text-align: left;
  height: 650px;
}
</style>


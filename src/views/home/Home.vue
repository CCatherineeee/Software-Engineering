<template>
  <div>
    <el-container>
      <el-aside width="150px">
        <div>
          <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            router
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-user-solid"></i>
                <span>账户</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/home/user/account">个人资料</el-menu-item>
                <el-menu-item index="2">设置</el-menu-item>
                <el-menu-item index="3">通知</el-menu-item>
                <el-menu-item index="3">文件</el-menu-item>
              </el-menu-item-group>
            </el-submenu>

            <el-menu-item index="/home/course">
              <i class="el-icon-school"></i>
              <span>课程</span>
            </el-menu-item>

            <el-menu-item index="2">
              <i class="el-icon-message"></i>
              <span>通知</span>
            </el-menu-item>

            <el-menu-item index="2">
              <i class="el-icon-document-copy"></i>
              <span>小组</span>
            </el-menu-item>

            <el-menu-item index="/login">退出</el-menu-item>
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

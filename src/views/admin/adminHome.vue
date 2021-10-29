<template>
  <el-scrollbar>
    <el-container style="height: 650px; background: #e6cfcc">
      <el-aside width="150px"></el-aside>
      <el-main>
        <el-header>
          <el-menu
            :default-active="activeIndex2"
            mode="horizontal"
            router
            background-color="#6A76AB"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/adminHome/accountAdd">创建账户</el-menu-item>
            <el-menu-item index="/adminHome/accountCheck"
              >查看信息</el-menu-item
            >
            <el-menu-item index="/adminHome/accountCancel"
              >注销账户</el-menu-item
            >
            <el-menu-item index="/login" style="float: right"
              >退出</el-menu-item
            >
          </el-menu>
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-main>
      <el-aside width="150px"></el-aside>
    </el-container>
  </el-scrollbar>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {},
};
</script>

<style >
.bg {
  background: #f88c6b;
  line-height: 570px;
}
</style>
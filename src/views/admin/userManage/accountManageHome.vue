<template>
  <el-container style="margin-top:20px;">
    <el-header>
      <el-menu
        mode="horizontal"
        router
        background-color="#5C6BC0"
        text-color="#fff"
        active-text-color="#ffd04b"
        :default-active="activeIndex"
      >
        <el-menu-item index="/adminHome/userManage/accountAdd"
          >创建账户</el-menu-item
        >
        <el-menu-item index="/adminHome/userManage/accountCheck"
          >查看信息</el-menu-item
        >
        <el-menu-item index="/adminHome/userManage/accountCancel"
          >注销账户</el-menu-item
        >
      </el-menu>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      activeIndex: this.$route.path,
    };
  },
  methods: {},
};
</script>
<template>
  <el-container style="margin-top: 20px">
    <el-header>
      <el-menu
        mode="horizontal"
        router
        background-color="#5C6BC0"
        text-color="#fff"
        active-text-color="#FFA000"
        :default-active="activeIndex"
      >
        <el-menu-item index="/adminHome/courseManage/courseType"
          >课程类型</el-menu-item
        >
        <el-menu-item index="/adminHome/courseManage/courseTea"
          >开课管理</el-menu-item
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

<style scoped>
</style>
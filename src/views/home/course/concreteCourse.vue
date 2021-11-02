<template>
  <el-container class="back">
    <el-header class="hBack">课程名称</el-header>
    <el-container>
      <el-aside width="120px" class="lBack">
        <el-menu
          default-active="2"
          @open="handleOpen"
          @close="handleClose"
          router
        >
          <el-menu-item index="/home/concreteCourse/Ann">
            <span slot="title">公告</span>
          </el-menu-item>
          <el-menu-item index="/home/concreteCourse/Exper">
            <span slot="title">实验</span>
          </el-menu-item>
          <el-menu-item index="">
            <span slot="title">评分</span>
          </el-menu-item>
          <el-menu-item index="/home/concreteCourse/Peo">
            <span slot="title">人员</span>
          </el-menu-item>
          <el-menu-item index="">
            <span slot="title">文件</span>
          </el-menu-item>
          <el-menu-item index="">
            <span slot="title">测验</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="mBack"> <router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.back {
  background: rgb(255, 255, 255);
  border-radius: 15px;
  height: 610px;
}
.hBack {
  padding: 20px;
  text-align: left;
  font: 20px Microsoft YaHei;
}
.lBack {
  padding: 20px;
  border-radius: 15px;
}
.mBack {
  padding: 20px;
}
.rBack {
  padding: 20px;
}
</style>
<template>
  <el-container class="back">
    <el-header class="hBack">课程名称</el-header>
    <el-container>
      <el-aside width="120px" class="lBack">
        <el-menu
            :default-active="activeIndex"
            @select="handleSelect"
        >
          <el-menu-item index="/studentHome/concreteCourse/Ann">
            <span slot="title">公告</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Exper">
            <span slot="title">实验</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Perform">
            <span slot="title">成绩</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/Peo">
            <span slot="title">人员</span>
          </el-menu-item>
          <el-menu-item index="/studentHome/concreteCourse/File">
            <span slot="title">文件</span>
          </el-menu-item>
          <el-menu-item index="">
            <span slot="title">测验</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="mBack">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data(){
    return{
      activeIndex : "",
      class_id : ""
    }
  },
  methods:{
    handleSelect(index){
      this.$router.push({path:index,
        query:{
          info : this.$Base64.encode(JSON.stringify({"class_id" : this.class_id}))}
      });
    }
  },
  mounted() {
    this.activeIndex = this.$route.path;
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id']
    console.log(this.class_id)
  }
}
</script>
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
  border-radius: 15px;
  box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15);
}
.rBack {
  padding: 20px;
}
</style>
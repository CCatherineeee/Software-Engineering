<template>
  <div >
    <h1 style="color: #409EFF;">控制面板</h1>
    <el-divider ></el-divider>
    <h3>欢迎！</h3>
    <el-container style="margin-top:20px;">
      <el-main >
        <el-calendar v-model="value"></el-calendar>
      </el-main>
    </el-container>


  </div>
</template>

<script>
export default {
  data() {
    return {
      value: new Date()
    }
  }
}
</script>
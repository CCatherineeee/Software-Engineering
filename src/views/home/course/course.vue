<template>
  <div>
    <el-row :gutter="20" v-for="o in 4" :key="o" class="text item">
      <el-col :span="6">
        <el-card shadow="hover"> Always </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"> Hover </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"> Never </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"> Never </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
</script>

<style >
.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 25px;
}
</style>
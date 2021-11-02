<template>
  <div>
    <el-row :gutter="30" v-for="(data, index) in courseData" :key="index">
      <el-col :span="8">
        <el-card shadow="hover" class="box-card">
          <template #header>
            <div class="card-header">
              <span>课程名字</span>
              <el-button type="text" @click="toCourse">查看</el-button>
            </div>
          </template>
          {{ data.name }}
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover" class="box-card">
          <template #header>
            <div class="card-header">
              <span>Card name</span>
              <el-button type="text" @click="toCourse">查看</el-button>
            </div>
          </template>
          {{ courseData[index].name }}
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover" class="box-card">
          <template #header>
            <div class="card-header">
              <span>Card name</span>
              <el-button class="button" type="text" @click="toCourse"
                >查看</el-button
              >
            </div>
          </template>
          {{ courseData[index].name }}
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      courseData: [
        {
          name: "1",
        },
        {
          name: "2",
        },
        {
          name: "3",
        },
        {
          name: "4",
        },
      ],
    };
  },
  methods: {
    toCourse() {
      this.$router.push("/home/concreteCourse");
    },
  },
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}

.box-card {
  width: 370px;
  height: 250px;
  border-radius: 10px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}
</style>
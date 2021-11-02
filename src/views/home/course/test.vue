<template>
  <el-row>
    <el-col
      v-for="(name, index) in courseData"
      :key="index"
      :span="8"
      :offset="index > 0 ? 2 : 0"
    >
      <el-card shadow="hover" class="box-card">
        <template #header>
          <div class="card-header">
            <span>Card name</span>
            <el-button class="button" type="text">Operation button</el-button>
          </div>
        </template>
        {{ courseData[index].name }}
      </el-card>
    </el-col>
  </el-row>
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
  methods: {},
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
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button {
  padding: 0;
  min-height: auto;
}
</style>

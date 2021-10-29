<template>
  <el-container>
    <el-main>
      <el-card>
        <el-descriptions title="账户信息" :column="2" border>
          <template slot="extra">
            <el-button type="primary" size="medium" @click="modifyAccount"
              >编辑</el-button
            >
          </template>
          <el-descriptions-item>
            <template slot="label"> 姓名 </template>
            {{ name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 学号 </template>
            {{ userID }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 性别 </template>
            {{ gender }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 手机号 </template>
            {{ phone }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 邮箱 </template>
            {{ email }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 状态 </template>
            <el-tag size="small">{{ state }}</el-tag>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"> 身份 </template>
            <el-tag size="small">{{ identity }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 学院 </template>
            {{ colleague }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 专业 </template>
            {{ major }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-main>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      name: "xzq",
      userID: 1951104,
      gender: "女",
      phone: 10086,
      email: "1@qq.com",
      state: "激活",
      identity: "学生",
      colleague: "软件",
      major: "软件",
    };
  },
  methods: {
    modifyAccount() {
      this.$router.push("/adminHome/accountModify");
    },
  },
};
</script>


<style scoped>
.demo-border .text {
  width: 15%;
}

.demo-border .line div {
  width: 100%;
  height: 0;
}
</style>

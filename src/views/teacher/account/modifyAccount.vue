<template>
  <el-container>
    <el-aside></el-aside>
    <el-main>
      <el-card style="box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15)">
        <el-form
          ref="userAccount"
          style="margin: 40px 100px 0px 50px"
          :model="userAccount"
          label-width="80px"
        >
          <el-form-item label="姓名" prop="name">
            <el-input type="text" v-model="userAccount.name"></el-input>
          </el-form-item>

          <el-form-item label="工号" prop="tid">
            <el-input v-model="userAccount.tid" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="学院" prop="college">
            <el-input v-model="userAccount.college" :disabled="true"></el-input>
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-select v-model="userAccount.gender" style="float: left">
              <el-option label="男" :value="1"></el-option>
              <el-option label="女" :value="0"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="手机" prop="phone">
            <el-input v-model="userAccount.phone"></el-input>
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input type="email" v-model="userAccount.email"></el-input>
          </el-form-item>

          <el-form-item>
            <el-button style="margin-left: 80px" @click="save()" type="primary"
              >保存修改</el-button
            >
            <el-button style="margin-left: 100px" @click="back">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
    <el-aside></el-aside>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      userAccount: {
        name: "",
        tid: "",

        gender: "",
        phone: "",
        email: "",
      },
    };
  },
  methods: {
    save() {},
    back() {
      this.$router.push("/teacherHome/teacher/passwordModify");
    },
  },
};
</script>

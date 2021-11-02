<template>
  <el-container>
    <el-aside></el-aside>
    <el-main>
      <el-card>
        <div class="grid-content bg-purple-dark">
          <el-form
            ref="userAccount"
            style="margin: 40px 100px 0px 50px"
            :model="userAccount"
            label-width="80px"
          >
            <el-form-item label="姓名" prop="name">
              <el-input type="text" v-model="userAccount.name"></el-input>
            </el-form-item>

            <el-form-item label="学号" prop="sid">
              <el-input type="number" v-model="userAccount.sid"></el-input>
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input
                type="password"
                v-model="userAccount.password"
              ></el-input>
            </el-form-item>

            <el-form-item label="学院" prop="college">
              <el-select
                v-model="userAccount.college"
                style="width: 100%"
                placeholder="请选择学院"
              >
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="性别" prop="gender">
              <el-select v-model="userAccount.gender" style="float: left">
                <el-option label="男" :value="1"></el-option>
                <el-option label="女" :value="0"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="手机" prop="phone">
              <el-input type="number" v-model="userAccount.phone"></el-input>
            </el-form-item>

            <el-form-item label="邮箱" prop="email">
              <el-input type="email" v-model="userAccount.email"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                style="margin-left: 80px"
                @click="save()"
                type="primary"
                >保存修改</el-button
              >
              <el-button style="margin-left: 100px" @click="back"
                >取消</el-button
              >
            </el-form-item>
          </el-form>
        </div>
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
        sid: 111,
        password: "",
        gender: "女",
        phone: 111,
        email: "",
      },
      options: [
        {
          value: "软件学院",
          label: "软件学院",
        },
        {
          value: "电信学院",
          label: "电信学院",
        },
        {
          value: "汽车学院",
          label: "汽车学院",
        },
        {
          value: "土木学院",
          label: "土木学院",
        },
        {
          value: "经管学院",
          label: "经管学院",
        },
        {
          value: "材料学院",
          label: "材料学院",
        },
        {
          value: "数学学院",
          label: "数学学院",
        },
        {
          value: "物理学院",
          label: "物理学院",
        },
        {
          value: "化学学院",
          label: "化学学院",
        },
      ],
    };
  },
  methods: {
    save() {},
    back() {
      this.$router.push("/home/student/account");
    },
  },
};
</script>

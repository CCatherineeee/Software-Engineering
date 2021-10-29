<template>
  <el-container>
    <el-main>
      <el-card style="margin: 0px 100px 0px 100px">
        <div class="grid-content bg-purple-dark">
          <p
            style="
              margin: 0px 0px 0px 0px;
              padding-top: 20px;
              color: black;
              font: 22px Microsoft YaHei;
              text-align: center;
            "
          >
            编辑信息
          </p>
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
              <el-input v-model="userAccount.sid"></el-input>
            </el-form-item>

            <el-form-item label="性别">
              <el-radio-group v-model="userAccount.gender">
                <el-radio label="男"></el-radio>
                <el-radio label="女"></el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="手机" prop="phone">
              <el-input v-model="userAccount.phone"></el-input>
            </el-form-item>

            <el-form-item label="邮箱" prop="email">
              <el-input type="email" v-model="userAccount.email"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                style="margin-left: 10px"
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
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      userAccount: {
        name: "",
        sid: 111,
        gender: "女",
        phone: 111,
        email: "",
      },
    };
  },
  methods: {
    save() {
      console.log(JSON.stringify(this.userAccount));

      this.axios
        .post("/api", JSON.stringify(this.userAccount))
        .then((response) => {
          //这里使用了ES6的语法
          console.log(response); //请求成功返回的数据
        });
    },

    back() {
      this.$router.push("/adminHome/accountInfo");
    },
  },
};
</script>

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

            <el-form-item label="学号" prop="id">
              <el-input v-model="userAccount.id"></el-input>
            </el-form-item>

            <el-form-item label="性别">
              <el-radio-group v-model="userAccount.gender">
                <el-radio label="男"></el-radio>
                <el-radio label="女"></el-radio>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="手机" prop="phone_number">
              <el-input v-model="userAccount.phone_number"></el-input>
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
import axios from "axios";
export default {
  data() {
    return {
      userAccount: {
        name: "",
        id: "",
        gender: "",
        phone_number: "",
        email: "",
        role: "",
      },
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      //var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内
      //console.log("传来的参数===" + routerParams);
      console.log("传来的id==" + this.$route.query.id);
      console.log("传来的role==" + this.$route.query.role);
      this.userAccount.id = this.$route.query.id;
      this.userAccount.role = this.$route.query.role;
    },

    getStuInfo() {
      if (this.userAccount.role == 1) {
        axios
          .get("/api/getUserInfo/Student/", {
            params: { s_id: this.userAccount.id },
            crossDomain: true,
          })
          .then((response) => {
            console.log("拿到的信息" + JSON.stringify(response.data));
            this.userAccount.name = response.data[0].name;
            this.userAccount.gender = response.data[0].gender;
            this.userAccount.phone_number = response.data[0].phone_number;
            this.userAccount.email = response.data[0].email;
            //this.userAccount.is_active = response.data[0].is_active;
            //this.role = response.data[0].role;
            //this.userAccount.department = response.data[0].department;
            //this.major_id;
          })
          .catch(function (error) {
            console(error);
          });
      } else if (this.userAccount.role == 2) {
        axios
          .get("/api/getUserInfo/Teacher/", {
            params: { t_id: this.userAccount.id },
            crossDomain: true,
          })
          .then((response) => {
            console.log("拿到的信息" + JSON.stringify(response.data));
            this.userAccount.name = response.data[0].name;
            this.userAccount.gender = response.data[0].gender;
            this.userAccount.phone_number = response.data[0].phone_number;
            this.userAccount.email = response.data[0].email;
            //this.userAccount.is_active = response.data[0].is_active;
            //this.role = response.data[0].role;
            //this.userAccount.department = response.data[0].department;
            //this.major_id;
          })
          .catch(function (error) {
            console(error);
          });
      } else if (this.userAccount.role == 3) {
        axios
          .get("/api/getUserInfo/TA/", {
            params: { ta_id: this.userAccount.id },
            crossDomain: true,
          })
          .then((response) => {
            console.log("拿到的信息" + JSON.stringify(response.data));
            this.userAccount.name = response.data[0].name;
            this.userAccount.gender = response.data[0].gender;
            this.userAccount.phone_number = response.data[0].phone_number;
            this.userAccount.email = response.data[0].email;
            //this.userAccount.is_active = response.data[0].is_active;
            //this.role = response.data[0].role;
            //this.userAccount.department = response.data[0].department;
            //this.major_id;
          })
          .catch(function (error) {
            console(error);
          });
      }
    },

    checkResponse(response) {
      if (response == "Success") this.$message("修改成功");
      else this.$message("错误");
    },

    save() {
      //保存修改
      if (this.userAccount.role == 1) {
        var jsons = {
          name: this.userAccount.name,
          s_id: this.userAccount.id,
          gender: this.userAccount.gender,
          phone_number: this.userAccount.phone_number,
          email: this.userAccount.email,
        };
      } else if (this.userAccount.role == 2) {
        jsons = {
          name: this.userAccount.name,
          t_id: this.userAccount.id,
          gender: this.userAccount.gender,
          phone_number: this.userAccount.phone_number,
          email: this.userAccount.email,
        };
      } else if (this.userAccount.role == 3) {
        jsons = {
          name: this.userAccount.name,
          ta_id: this.userAccount.id,
          email: this.userAccount.email,
        };
      }

      if (this.userAccount.role == 1) {
        this.axios
          .post("/api/editInfo/Student/", JSON.stringify(jsons))
          .then((response) => {
            this.checkResponse(response.data); //请求成功返回的数据
          });
      } else if (this.userAccount.role == 2) {
        this.axios
          .post("/api/editInfo/Teacher/", JSON.stringify(jsons))
          .then((response) => {
            this.checkResponse(response.data); //请求成功返回的数据
          });
      } else if (this.userAccount.role == 3) {
        this.axios
          .post("/api/editInfo/TA/", JSON.stringify(jsons))
          .then((response) => {
            this.checkResponse(response.data); //请求成功返回的数据
          });
      }
      document.execCommand("Refresh");
      this.$router.push({
        path: "/adminHome/userManage/accountInfo",
        query: { id: this.userAccount.id, role: this.userAccount.role },
      });
    },

    back() {
      this.$router.push({
        path: "/adminHome/userManage/accountInfo",
        query: { id: this.userAccount.id, role: this.userAccount.role },
      });
    },
  },
  mounted() {
    this.getParams();
    this.getStuInfo();
  },
};
</script>

<!-- 个人信息页面-->
<template>
  <el-container style="margin-top: 20px">
    <el-aside width="200px"></el-aside>
    <el-main class="back">
    <div class="circle" @click.stop="uploadHeadImg">
        <div class="circle0" v-html="avatar"></div>
        <div class="circle1">修改头像</div>
      </div>
      <input
        type="file"
        accept="image/*"
        @change="handleFile"
        class="hiddenInput"
      />
      <el-card style="box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15)">
        <el-descriptions
          title="账户信息"
          :column="2"
          border
          size="medium"
          box-shadow="15px 15px 10px"
        >
          <template slot="extra">
            <el-button type="primary" size="medium" @click="modifyAccount()"
              >编辑</el-button
            >
          </template>
          <el-descriptions-item>
            <template slot="label"> 姓名 </template>
            {{ name }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 工号 </template>
            {{ id }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 性别 </template>
            {{ gender }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 手机号 </template>
            {{ phone_number }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 邮箱 </template>
            {{ email }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template slot="label"> 状态 </template>
            <el-tag
              :type="is_active === 1 ? 'success' : 'danger'"
              disable-transitions
              ><span v-if="is_active === 1">激活</span>
              <span v-if="is_active === 0">非激活</span></el-tag
            >
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-main>
    <el-aside width="200px"></el-aside>
  </el-container>
</template>


<script>
export default {
  data() {
    return {
      name: "",
      id: "",
      gender: "",
      phone_number: "",
      email: "",
      is_active: "",
      //role: "",
      department: "",
      avatar: "",
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    getUserAvatar: function () {
      let param = new FormData(); // 创建form对象
      param.append("t_id", sessionStorage.getItem("id"));
      this.axios
        .post("/api/getUserInfo/Teacher/showAvatar", param)
        .then((response) => {
          var address = "http://39.107.51.181:5000";
          var url = response.data.url;
          var imgHtml = "<img src=" + address + url + "></img>";
          console.log(imgHtml);
          this.avatar = imgHtml;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getTeaInfo() {
      this.axios
        .get("/api/getUserInfo/Teacher/", {
          params: { t_id: this.id, token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          console.log(response);

          this.name = response.data[0].name;
          this.gender = response.data[0].gender;
          this.phone_number = response.data[0].phone_number;
          this.email = response.data[0].email;
          this.is_active = response.data[0].is_active;
          //this.role = response.data[0].role;
          this.department = response.data[0].department;
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/teacherHome/modifyAccount",
      });
    },
        // 打开图片上传
    uploadHeadImg: function () {
      this.$el.querySelector(".hiddenInput").click();
    },
    // 将头像显示
    handleFile: function (e) {
      let $target = e.target || e.srcElement;
      let file = $target.files[0];
      let param = new FormData(); // 创建form对象
      param.append("avatar", file); // 将文件存入file下面
      param.append("token", sessionStorage.getItem("token"));
      param.append("id", sessionStorage.getItem("id"));
      let config = { headers: { "Content-Type": "multipart/form-data" } };
      this.axios
        .post("/api/editInfo/uploadAvatar", param, config)
        .then((response) => {
          var msg = response.data.message;
          this.$message(msg);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  mounted() {
    this.getParams();
    this.getTeaInfo();
    this.getUserAvatar();
  },
};
</script>


<style scoped>
.circle {
  margin: 0 auto;
  width: 220px;
  height: 220px;
  position: relative;
  overflow: hidden;
}
.circle0 {
  width: 220px;
  height: 220px;
  /* background-color: red; */
  background-size: 100% 100%;
}
.circle1 {
  width: 220px;
  height: 220px;
  background-color: #999999;
  opacity: 0.6;
  transition: transform 1s ease;
  text-align: center;
  display: -moz-box; /*兼容Firefox*/
  display: -webkit-box; /*兼容FSafari、Chrome*/

  -moz-box-align: center; /*兼容Firefox*/
  -webkit-box-align: center; /*兼容FSafari、Chrome */

  -moz-box-pack: center; /*兼容Firefox*/
  -webkit-box-pack: center; /*兼容FSafari、Chrome */
  color: #ffffff;
}
.circle:hover > .circle1 {
  transform: translateY(-100%);
}
.back {
  width: 700px;
}
.demo-border .text {
  width: 15%;
}
.hiddenInput {
  display: none;
}

.demo-border .line div {
  width: 100%;
  height: 0;
}
.el-button--primary {
  color: white;
}
</style>

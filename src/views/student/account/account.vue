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
      <div style="margin-top: 25px">
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
              <template slot="label"> 学号 </template>
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

            <el-descriptions-item>
              <template slot="label"> 学院 </template>
              {{ department }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template slot="label"> 专业 </template>
              {{ major_id }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </div>
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
      major_id: "",
      avatar: "",
    };
  },
  methods: {
    getUserAvatar: function () {
      let param = new FormData(); // 创建form对象
      param.append("s_id", sessionStorage.getItem("id"));
      this.axios
        .post("/api/getUserInfo/Student/showAvatar", param)
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
    getParams: function () {
      this.id = sessionStorage.getItem("id");
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

      var reader = new FileReader();
      // reader.onload = (data) => {
      //   let res = data.target || data.srcElement
      //   // this.userInfo.avatar = res.result
      // }

      reader.readAsDataURL(file);
    },

    getStuInfo() {
      this.axios
        .post(
          "/api/getUserInfo/Student/",
          JSON.stringify({
            s_id: this.id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("getStuInfo", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.name = response.data["data"][0].name;
            this.gender = response.data["data"][0].gender;
            this.phone_number = response.data["data"][0].phone_number;
            this.email = response.data["data"][0].email;
            this.is_active = response.data["data"][0].is_active;
            //this.role = response.data[0].role;
            this.department = response.data["data"][0].department;
            //this.major_id;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    modifyAccount() {
      this.$router.push({
        path: "/studentHome/modifyAccount",
      });
    },
  },
  mounted() {
    this.getParams();
    this.getStuInfo();
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
  margin-top: 20px;
}
.demo-border .text {
  width: 15%;
}

.demo-border .line div {
  width: 100%;
  height: 0;
}

.hiddenInput {
  display: none;
}
.caption {
  color: #8f8f8f;
  font-size: 26px;
  height: 37px;
}
.el-button--primary {
  color: white;
}
</style>

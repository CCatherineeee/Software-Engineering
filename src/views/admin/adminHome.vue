<template>
  <div>
    <el-container class="back">
      <el-aside width="15%">
        <div>
          <el-menu class="admin-aside-menu" router>
            <img
              src="https://www.w3school.com.cn/i/photo/coffee.jpg"
              class="admin-aside-menu-head"
            />
            <el-submenu index="">
              <template slot="title">
                <i class="el-icon-edit"></i>
                <span>个人信息</span>
              </template>
              <el-menu-item-group>
                <el-menu-item index="/adminHome/account"
                  >查看个人资料</el-menu-item
                >
                <el-menu-item index="/adminHome/modifyPassword"
                  >修改密码</el-menu-item
                >
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="/adminHome/userManage/accountAdd">
              <i class="el-icon-user"></i>
              <span slot="title">用户管理</span>
            </el-menu-item>
            <el-menu-item index="/adminHome/courseManage/courseType">
              <i class="el-icon-reading"></i>
              <span slot="title">课程管理</span>
            </el-menu-item>
            <el-menu-item index="/adminHome/annManage">
              <i class="el-icon-postcard"></i>
              <span slot="title">公告管理</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<style scoped>
.el-main {
  background-color: #ffffff;

  height: 650px;
  border-radius: 20px;
}
.back {
  margin-left: 10px;
}
.admin-aside-menu {
  box-shadow: 3px 3px 10px #d3d3d3;
  background: rgb(255, 255, 255);
  border-radius: 10%;
}
.admin-aside-menu-head {
  margin: 20px auto;
  width: 70%;
  height: 150px;
  border-radius: 50%;
}
</style>

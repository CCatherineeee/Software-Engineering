<template>
  <div id="test">
    <div>
      <el-row>
        <el-col>

        </el-col>
      </el-row>
    </div>
    <div id="app">
      <el-row>
        <el-col :span="24"
          ><div class="grid-content bg-purple-dark"></div
        ></el-col>
      </el-row>
      <div id="nav">
        <router-link to="/studentHome/account">Stuent-Home</router-link> |
        <router-link to="/teacherHome">Teacher-Home</router-link> |
        <router-link to="/adminHome">Admin-Home</router-link> |
        <router-link to="/login">Login-test</router-link>
      </div>
      <router-view />
    </div>
  </div>
</template>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

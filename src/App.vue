<template>
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
      <router-link to="/assistHome">assist-Home</router-link> |
      <router-link to="/test">在线编译器test</router-link> |
      <router-link to="/login">Login-test</router-link>
    </div>
    <router-view />
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
  background: -webkit-gradient(
    linear,
    left top,
    left bottom,
    color-stop(0%, #8ab9eb),
    color-stop(40%, #5c9ddc),
    color-stop(100%, #2374c5)
  );
  box-shadow: 2px 2px 2px #888888;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

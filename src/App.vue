<template>
  <div id="app">
    <el-row>
      <el-col :span="24"
        ><div class="grid-content bg-purple-dark"></div
      ></el-col>
    </el-row>
    <div id="nav">
      <a href="/"><img src="@/assets/SystemLogo.png" /></a>
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
  color: #f8f8f8;
}
</style>

<template>
  <div>
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="活动名称">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="get_data">立即创建</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
//import axios from "axios";

export default {
  data() {
    return {
      form: {
        name: "123",
      },
    };
  },

  methods: {
    get_data() {
      this.axios({
        method: "get",
        url: "http://127.0.0.1:5000/test1",
        crossDomain: true,
        crossOrigin: true,
        params: {
          name: JSON.stringify(this.form.name),
        },
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
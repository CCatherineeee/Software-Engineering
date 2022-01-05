<!-- 教师查看自己名下所有班级 -->
<template>
  <v-row>
    <v-col v-for="index in classData" :key="index.class_id">
      <v-card max-width="344px">
        <v-img
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        ></v-img>

        <v-card-title>
          {{ index.course_name }}
          {{ index.class_id }}
        </v-card-title>

        <v-card-subtitle>
          {{ index.year }} 年 {{ index.semester }}</v-card-subtitle
        >

        <v-card-actions>
          <v-btn color="orange lighten-2" @click="toClass(index)"> 查看 </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      classData: [],
      id: "",
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    getClass() {
      var jsons = {
        t_id: this.id,
        token: sessionStorage.getItem("token"),
      };
      console.log("获得班级");
      console.log(jsons);
      this.axios
        .post("/api/manageClass/teacherGetClass", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] == 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else if (response.data["code"] == 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          }
          this.classData = response.data.data;
        });
    },

    toClass(index) {
      console.log(index);
      this.$router.push({
        path: "/teacherHome/concreteCourse/Ann",
        //query: { c_id: this.$Base64.encode(index.class_id) },
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ class_id: index.class_id })
          ),
        },
      });
    },
  },
  mounted() {
    this.getParams();
    this.getClass();
  },
};
</script>

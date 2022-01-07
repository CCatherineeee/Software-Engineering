<!-- 助教查看自己名下所有班级 -->
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
      classData: [
        {
          class_id: 0,
          class_number: 0,
          course_name: "默认",
          prefix: "0",
          semester: "学期",
          year: "year",
        },
      ],
      id: "",
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    getClass() {
      var jsons = {
        ta_id: this.id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/TAGetClass", JSON.stringify(jsons))
        .then((response) => {
          console.log("获得班级", response);
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
      console.log("toClass", index);
      this.$router.push({
        path: "/assistHome/concreteCourse/Ann",
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

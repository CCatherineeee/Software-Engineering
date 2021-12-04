
<template>
  <v-row>
    <v-col v-for="index in courseData" :key="index">
      <v-card class="mx-auto" max-width="344">
        <v-img
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        ></v-img>

        <v-card-title>
          {{ index.course_name }}
          {{index.class_id }}
          <v-spacer></v-spacer>

        </v-card-title>

        <v-card-subtitle> {{ index.year }} 年  {{ index.semester }}</v-card-subtitle>

        <v-card-actions>
          <v-btn color="orange lighten-2" @click="toCourse(index)"> 查看 </v-btn>

          <v-spacer></v-spacer>

          <v-btn icon @click="show = !show">
            <v-icon>{{ show ? "mdi-chevron-up" : "mdi-chevron-down" }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <div v-show="show">
            <v-divider></v-divider>

            <v-card-text> 课程简介 </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>

export default {
  data() {
    return {
      show: false,
      courseData: [],
      id:""
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem('id');
    },
    getCourse(){
      this.axios.post('/api/manageClass/teacherGetClass',JSON.stringify({
        t_id : sessionStorage.getItem('id'),
        token : sessionStorage.getItem('token')
      })).then((response) => {
        if(response.data['code'] == 404){
          this.$message("找不到页面")
          this.$router.push({path:"/404"})
        }
        else if(response.data['code'] == 301){
          this.$message("验证过期")
          this.$router.push({path:"/login"})
        }
        this.courseData = response.data['data'] //请求成功返回的数据
      });
    },

    toCourse(index) {
      this.$router.push({path:"/teacherHome/concreteCourse",
        query:{
          info : this.$Base64.encode(JSON.stringify({"class_id" : index.class_id}))}
      });
    },
  },
  mounted() {
    this.getParams();
    this.getCourse();
  },
};
</script>

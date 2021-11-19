
<template>
  <v-row>
    <v-col v-for="index in courseData" :key="index">
      <v-card class="mx-auto" max-width="344">
        <v-img
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        ></v-img>

        <v-card-title>
          {{ index.title }}
          <v-spacer></v-spacer>
          <v-btn class="ma-2" color="red" dark float="right">
            {{ index.role }}
          </v-btn>
        </v-card-title>

        <v-card-subtitle> {{ index.place }}{{ index.time }}</v-card-subtitle>

        <v-card-actions>
          <v-btn color="orange lighten-2" @click="toCourse"> 查看 </v-btn>

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
      courseData: [
        {
          title: "课程名称1",
          place: "上课地点1",
          time: "上课时间1",
          role: "责任教师",
        },
        {
          title: "课程名称2",
          place: "上课地点2",
          time: "上课时间2",
          role: "教师",
        },
        {
          title: "课程名称3",
          place: "上课地点3",
          time: "上课时间3",
          role: "教师",
        },
        {
          title: "课程名称4",
          place: "上课地点4",
          time: "上课时间4",
          role: "责任教师",
        },
      ],
    };
  },
  methods: {
    toCourse() {
      this.$router.push("/teacherHome/concreteCourse");
    },
  },
};
</script>

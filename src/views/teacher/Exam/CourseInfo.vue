<template>
  <div>
    <el-descriptions
        :column="1"
        border
        style="margin-bottom: 10px; margin-top: 10px"
        title="课程信息">
      <el-descriptions-item label="课程id">{{course_id}}</el-descriptions-item>
      <el-descriptions-item label="课程名称">{{name}}</el-descriptions-item>
      <el-descriptions-item label="责任教师" :span="2">{{id }}</el-descriptions-item>
      <el-descriptions-item label="上课时间">
        {{ year }}年 {{ semester }}
      </el-descriptions-item>
      <el-descriptions-item label="各项成绩占比">
        考试： {{ semester }}<br />
        实验： {{ semester }}<br />
        出勤： {{ semester }}
      </el-descriptions-item>
    </el-descriptions>
    <div>
      <v-btn dark @click="handleScore">修改成绩占比</v-btn>
    </div>

    <div>
      <el-dialog
          :visible.sync="scoreDialog"
          title="设置成绩占比（以小数形式）"
          center
          width="50%">
        <v-container>
          <el-input
              label="考试"
              v-model="eachScore.exam"
          ></el-input>

          <el-input
              filled
              label="实验"
              auto-grow
              height="20px"
              v-model="eachScore.report"
          ></el-input>

          <el-input
              filled
              label="出勤"
              auto-grow
              height="20px"
              v-model="eachScore.attendance"
          ></el-input>
        </v-container>

        <div slot="footer" class="dialog-footer">
          <el-button @click="scoreDialog = false">取消</el-button>
          <el-button type="primary" @click="setScore()">确定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>

</template>

<script>
export default {
  name: "CourseInfo",
  data(){
    return{
      course_id:"",
      name:"",
      year:"",
      semester:"",
      id:"",
      scoreDialog:false,
      eachScore: {
        exam: "",
        report: "",
        attendance: "",
      },
    }
  },
  methods: {
    getParams: function () {

      this.course_id = JSON.parse(this.$Base64.decode(this.$route.query.info)).course_id;
      this.name = JSON.parse(this.$Base64.decode(this.$route.query.info)).name;
      this.year = JSON.parse(this.$Base64.decode(this.$route.query.info)).year;
      this.semester = JSON.parse(this.$Base64.decode(this.$route.query.info)).semester;
      this.id = sessionStorage.getItem("id");
      console.log("test"+JSON.parse(this.$Base64.decode(this.$route.query.info)))
    },
    handleScore(){

    }
  },
  mounted() {
    this.getParams()

  }
}
</script>

<style scoped>

</style>

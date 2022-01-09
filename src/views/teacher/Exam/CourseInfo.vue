<template>
  <div>
    <el-descriptions
      :column="1"
      border
      style="margin-bottom: 10px; margin-top: 10px"
      title="课程信息"
    >
      <el-descriptions-item label="课程id">{{
        course_id
      }}</el-descriptions-item>
      <el-descriptions-item label="课程名称">{{ name }}</el-descriptions-item>
      <el-descriptions-item label="责任教师" :span="2">{{
        id
      }}</el-descriptions-item>
      <el-descriptions-item label="上课时间">
        {{ year }}年 {{ semester }}
      </el-descriptions-item>
      <el-descriptions-item label="各项成绩占比">
        考试： {{ eachScore.exam }}<br />
        实验： {{ eachScore.report }}<br />
        出勤： {{ eachScore.attendance }}
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
        width="50%"
      >
        <v-container>
          <v-text-field
            label="考试"
            auto-grow
            filled
            v-model="eachScore.exam"
            row-height="20"
          ></v-text-field>

          <v-text-field
            label="实验"
            auto-grow
            filled
            v-model="eachScore.report"
            row-height="20"
          ></v-text-field>
          <v-text-field
            label="出勤"
            auto-grow
            filled
            v-model="eachScore.attendance"
            row-height="20"
          ></v-text-field>
        </v-container>

        <div slot="footer" class="dialog-footer">
          <el-button @click="scoreDialog = false">取消</el-button>
          <el-button type="primary" @click="setPercent()">确定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: "CourseInfo",
  data() {
    return {
      course_id: "",
      name: "",
      year: "",
      semester: "",
      id: "",
      scoreDialog: false,
      eachScore: {
        exam: 0,
        report: 0,
        attendance: 0,
      },
    };
  },
  methods: {
    getParams: function () {
      this.course_id = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).course_id;
      this.name = JSON.parse(this.$Base64.decode(this.$route.query.info)).name;
      this.year = JSON.parse(this.$Base64.decode(this.$route.query.info)).year;
      this.semester = JSON.parse(
        this.$Base64.decode(this.$route.query.info)
      ).semester;
      this.id = sessionStorage.getItem("id");
      //console.log("test"+JSON.parse(this.$Base64.decode(this.$route.query.info)))
    },
    handleScore() {
      this.scoreDialog = true;
    },
    getPercent() {
      var json = {
        course_id: this.course_id,
      };
      this.axios
        .post("/api/weight/get", JSON.stringify(json))
        .then((response) => {
          console.log("getPercent", response);
          this.eachScore.exam = response.data.data.exam_weight;
          this.eachScore.report = response.data.data.experiment_weight;
          this.eachScore.attendance = response.data.data.attendence_weight;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setPercent() {
      //设置成绩占比
      var exam = this.eachScore.exam * 1;
      var report = this.eachScore.report * 1;
      var attendance = this.eachScore.attendance * 1;
      console.log("percent", exam + report + attendance);
      if (
        exam + report + attendance < 0.9999999999999999 ||
        exam + report + attendance > 1
      ) {
        this.$message.warning("所有成绩占比加合不为1，请重新输入！");
      } else {
        var json = {
          course_id: this.course_id,
          exam_weight: this.eachScore.exam,
          experiment_weight: this.eachScore.report,
          attendence_weight: this.eachScore.attendance,
        };
        this.axios
          .post("/api/weight/set", JSON.stringify(json))
          .then((response) => {
            console.log("setPercent", response);
            this.$message.success("修改成功！");
            this.scoreDialog = false;
            this.getPercent();
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
  },
  mounted() {
    this.getParams();
    this.getPercent();
  },
};
</script>

<style scoped>
</style>

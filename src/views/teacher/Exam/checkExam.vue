<template>
  <el-table :data="examList">
    <el-table-column prop="title" label="名称" width="170"> </el-table-column>
    <el-table-column prop="start_time" label="起始时间" width="180">
    </el-table-column>
    <el-table-column prop="end_time" label="截止时间" width="180" sortable>
    </el-table-column>
    <el-table-column width="80" prop="status" label="状态" sortable>
      <template #default="scope">
        <el-tag :key="scope.row.status" :type="scope.row.type" effect="plain">
          {{ scope.row.status }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <div v-if="scope.row.status === '未开放'">
          <el-button type="primary" @click="editExamTime(scope.row)"
            >修改</el-button
          >
          <el-button type="primary" @click="pushExamSendMsg(scope.row)"
            >开放</el-button
          >
          <el-button type="primary" @click="lookExam(scope.row)"
            >查看</el-button
          >
        </div>
        <div v-if="scope.row.status === '进行中'">
          <el-button type="primary" @click="stopExam(scope.row)"
            >中止</el-button
          >
          <el-button type="primary" @click="lookExam(scope.row)"
            >查看</el-button
          >
        </div>
        <div v-if="scope.row.status === '已截止'">
          <el-button type="primary" @click="editExamTime(scope.row)"
            >修改</el-button
          >

          <el-button type="primary" @click="lookExam(scope.row)"
            >查看</el-button
          >

          <el-button type="primary" @click="deleteExam(scope.row)"
          >删除</el-button
          >
        </div>

        <el-dialog title="修改起始、截至日期" :visible.sync="dialogVisible">
          <el-date-picker
            v-model="edit_start_time"
            type="datetime"
            placeholder="选择开始日期"
            style="margin-bottom: 15px; width: 50%"
          >
          </el-date-picker>
          <br />
          <el-date-picker
            v-model="edit_end_time"
            type="datetime"
            placeholder="选择截止日期"
            style="margin-bottom: 15px; width: 50%"
          >
          </el-date-picker>
          <br />
          <br />
          <el-button @click="submitEditExam" type="primary">确认</el-button>
        </el-dialog>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "checkExam",
  data() {
    return {
      examList: [],
      course_id: "",
      courseName: "",
      dialogVisible: false,
      edit_start_time: null,
      edit_end_time: null,
      edit_exam_id: null,
      stu_list: [],
      addSuccess: false,
    };
  },
  methods: {
    getExamList() {
      this.axios
        .post(
          "/api/getExam",
          JSON.stringify({
            course_id: this.course_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((res) => {
          console.log("getExamList()", res, this.course_id);
          if (res.data.code === 200) {
            this.examList = [];
            if (res.data.data.role !== 2) {
              this.$router.push({
                path: "/404",
              });
            }
            for (var i = 0; i < res.data.data.data.length; i++) {
              if (res.data.data.data[i].status === 0) {
                res.data.data.data[i].status = "未开放";
                res.data.data.data[i].type = "warning";
              } else if (res.data.data.data[i].status === 1) {
                res.data.data.data[i].status = "进行中";
                res.data.data.data[i].type = "success";
              } else {
                res.data.data.data[i].status = "已截止";
                res.data.data.data[i].type = "danger";
              }

              this.examList.push(res.data.data.data[i]);
            }
          }
        });
    },
    getParams: function () {
      this.course_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "course_id"
      ];
    },
    async pushExamSendMsg(row) {
      await this.pushExam(row);
      await this.examGetStudent(row);
      await this.classGetCourseName();
      await this.sendStuMessage(row);
    },
    examGetStudent(row) {
      //获取所有学生
      var exam_id = row.exam_id;
      var json = {
        exam_id: exam_id,
      };
      return (
        this.axios
          //.post("/api/course/addEx/", JSON.stringify(jsons))
          .post("/api/exam/examGetStudent", JSON.stringify(json))
          .then((response) => {
            if (response.data["code"] === 400) {
              this.$message("考试不存在");
            } else {
              var class_student = response.data["data"];
              //求并集
              console.log(class_student);
              for (var t = 0; t < class_student.length; t++) {
                this.stu_list.push(class_student[t]);
              }
            }
          })
      );
    },
    sendStuMessage(row) {
      //在这里添加，获取所有学生还要再写一个接口！！
      var end_time = this.getDate(row.end_time);
      var date = this.formatDateTime(end_time);
      console.log(end_time);
      if (this.addSuccess == true) {
        for (var i = 0; i < this.stu_list.length; i++) {
          var content =
            this.courseName + "已发布考试" + ",请在" + row.end_time + "前完成";
          var json4 = {
            s_id: this.stu_list[i]["s_id"],
            title: this.courseName + "已新增考试",
            content: content,
            deadline: date,
          };
          this.axios
            //.post("/api/course/addEx/", JSON.stringify(jsons))
            .post("/api/message/addStuMessage", JSON.stringify(json4))
            .then((response) => {
              if (response.data["code"] === 400) {
                this.$message("找不到学生");
              } else {
                console.log(response.data["message"]);
              }
            });
        }
      }
    },
    classGetCourseName() {
      var json = {
        course_id: this.course_id,
      };
      return (
        this.axios
          //.post("/api/course/addEx/", JSON.stringify(jsons))
          .post("/api/manageClass/IDGetClass", JSON.stringify(json))
          .then((response) => {
            if (response.data["code"] === 500) {
              this.$message("班级不存在");
            } else {
              var course = response.data["data"];
              //求并集
              console.log(course);
              this.courseName = course.course_name;
            }
          })
      );
    },
    pushExam(row) {
      this.addSuccess = false;
      this.axios
        .post(
          "/api/pushExamForce",
          JSON.stringify({
            exam_id: row.exam_id,
            course_id: this.course_id,
          })
        )
        .then((res) => {
          console.log(res);
          if (res.data.code === 200) {
            this.getExamList();
            this.addSuccess = true;
          }
        });
    },
    lookExam(row) {
      this.$router.push({
        path: "/teacherHome/concreteCourse/exam",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ exam_id: row.exam_id, course_id: this.course_id })
          ),
        },
      });
    },
    stopExam(row) {
      this.axios
        .post(
          "/api/stopExam",
          JSON.stringify({
            exam_id: row.exam_id,
          })
        )
        .then((res) => {
          console.log(res);
          if (res.data.code === 200) {
            this.getExamList();
          }
        });
    },
    editExamTime(row) {
      this.dialogVisible = true;
      this.edit_exam_id = row.exam_id;
    },
    submitEditExam() {
      this.dialogVisible = false;
      this.axios
        .post(
          "/api/editExamTime",
          JSON.stringify({
            exam_id: this.edit_exam_id,
            start_time: this.formatDateTime(this.edit_start_time),
            end_time: this.formatDateTime(this.edit_end_time),
            course_id: this.course_id,
          })
        )
        .then((res) => {
          if (res.data.code === 200) {
            this.$message("修改成功！");
            this.getExamList();
          } else {
            this.$message("修改失败");
          }
          this.edit_start_time = null;
          this.edit_end_time = null;
          this.edit_exam_id = null;
        });
    },
    getDate(strDate) {
      if (strDate) {
        var arr1 = strDate.split(" ");
        var sdate = arr1[0].split("-");
        var date = new Date(sdate[0], sdate[1] - 1, sdate[2]);
        return date;
      }
    },
    formatDateTime(date) {
      //时间戳转换
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      var d = date.getDate();
      d = d < 10 ? "0" + d : d;
      var h = date.getHours();
      h = h < 10 ? "0" + h : h;
      var minute = date.getMinutes();
      minute = minute < 10 ? "0" + minute : minute;
      var second = date.getSeconds();
      second = second < 10 ? "0" + second : second;
      return y + "-" + m + "-" + d + " " + h + ":" + minute + ":" + second;
    },
    deleteExam(row){
      this.axios.post("/api/delExam",JSON.stringify({
        exam_id:row.exam_id,
        token:sessionStorage.getItem('token')
      })).then((res)=>{
        if(res.data.code === 200){
          this.$message("删除成功")
          this.getExamList()
        }
        else{
          this.$message("没有权限")
        }
      }).catch((err)=>{
        console.log(err)
        this.$message("网络错误")
      })
    }
  },
  mounted() {
    this.getParams();
    this.getExamList();
  },
};
</script>

<style scoped>
.el-button--primary {
  color: white;
}
</style>

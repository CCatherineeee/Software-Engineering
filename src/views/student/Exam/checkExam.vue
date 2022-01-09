<template>
  <div>
    <el-table :data="examList">
      <el-table-column prop="title" label="名称" width="170"> </el-table-column>
      <el-table-column prop="start_time" label="起始时间" width="180">
      </el-table-column>
      <el-table-column prop="end_time" label="截止时间" width="180">
      </el-table-column>
      <el-table-column width="80" prop="status" label="状态">
        <template #default="scope">
          <el-tag :key="scope.row.status" :type="scope.row.type" effect="plain">
            {{ scope.row.status }}
          </el-tag>
          <el-tag
            :key="scope.row.submitStauts"
            :type="scope.row.submitType"
            effect="plain"
          >
            {{ scope.row.submitStauts }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="score" label="分数" width="180"> </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <div v-if="scope.row.submitStauts === '已提交'">
            <el-button type="primary" @click="lookCloseExam(scope.row)"
              >查看</el-button
            >
          </div>
          <div v-else-if="scope.row.status === '进行中'">
            <el-button type="primary" @click="lookExam(scope.row)"
              >进入</el-button
            >
          </div>
          <div v-else-if="scope.row.status === '已截至'">
            <el-button type="primary" @click="lookCloseExam(scope.row)"
              >查看</el-button
            >
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "checkExam",
  data() {
    return {
      examList: [],
      course_id: "",
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
          console.log("getExamList", res, this.course_id);
          if (res.data.code === 200) {
            this.examList = [];
            if (res.data.data.role !== 1) {
              this.$router.push({
                path: "/404",
              });
            }
            for (var i = 0; i < res.data.data.data.length; i++) {
              if (res.data.data.data[i].status === 0) {
                continue;
              } else if (res.data.data.data[i].status === 1) {
                res.data.data.data[i].status = "进行中";
                res.data.data.data[i].type = "success";
              } else {
                res.data.data.data[i].status = "已截至";
                res.data.data.data[i].type = "danger";
              }

              if (res.data.data.data[i].is_submit === 0) {
                res.data.data.data[i].submitStauts = "未提交";
                res.data.data.data[i].submitType = "warning";
              } else {
                res.data.data.data[i].submitStauts = "已提交";
                res.data.data.data[i].submitType = "success";
              }

              if (res.data.data.data[i].score === null) {
                res.data.data.data[i].score = 0;
                res.data.data.data[i].submitType = "warning";
              }

              this.examList.push(res.data.data.data[i]);
            }
          }
        });
    },
    getParams() {
      var class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      this.course_id = class_id.substring(0, 12);
    },

    lookExam(row) {
      this.$alert(
        "系统会随机对班级成员进行分组，以2-3人为一组，组内进行对抗。对抗练习的分数计算规则为：总得分*排名权重，第一名为1，第二名为0.9，第三名为0.8。",
        "对抗练习须知",
        {
          confirmButtonText: "确定",
          callback: (action) => {
            console.log(action);
            this.$router.push({
              path: "/studentHome/concreteCourse/examHome/exam",
              query: {
                info: this.$Base64.encode(
                  JSON.stringify({
                    exam_id: row.exam_id,
                    course_id: this.course_id,
                  })
                ),
              },
            });
          },
        }
      );
    },
    lookCloseExam(row) {
      this.$router.push({
        path: "/studentHome/concreteCourse/examHome/closeExam",
        query: {
          info: this.$Base64.encode(JSON.stringify({ exam_id: row.exam_id })),
        },
      });
    },
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

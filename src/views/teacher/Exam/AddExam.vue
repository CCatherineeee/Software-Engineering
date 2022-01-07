<template>
  <el-form :model="ruleForm" ref="ruleForm">
    <div>
      <el-input placeholder="请输入测验标题" v-model="ex_title"></el-input>
      <br />
      <br />
      <el-date-picker
        v-model="start_time"
        type="datetime"
        placeholder="选择开始日期"
        style="margin-bottom: 15px; width: 50%"
      >
      </el-date-picker>
      <br />
      <el-date-picker
        v-model="end_time"
        type="datetime"
        placeholder="选择截止日期"
        style="margin-bottom: 15px; width: 50%"
      >
      </el-date-picker>
    </div>
    <div v-for="(item, index) in questionList" :key="index">
      <el-card>
        <div>
          <el-row>
            <!-- 题目的信息 -->
            <el-col :span="20">
              <p style="font-weight: 700">第{{ index + 1 }}题</p>
            </el-col>
            <el-col :span="3">
              <el-button type="primary" @click="removeItem(index)"
                >删除</el-button
              >
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <br />
            <el-col :span="3">
              <el-input placeholder="分值" v-model="item.q_score"></el-input>
            </el-col>
          </el-row>

          <br />
          <el-radio-group v-model="item.q_type">
            <el-radio label="1">单选</el-radio>
            <el-radio label="2">多选</el-radio>
            <el-radio label="3">判断</el-radio>
          </el-radio-group>
          <br />
          <br />
          <p>题目描述</p>
          <br />
          <el-input
            label="请输入题目描述"
            type="textarea"
            :rows="2"
            v-model="item.title"
          ></el-input>
        </div>
        <br />
        <br />
        <div v-if="item.q_type === '1'">
          <el-form-item prop="resource">
            <p>请输入选项并选择正确答案</p>
            <el-radio-group v-model="item.answer">
              <el-radio label="1">
                A.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_a"
                ></el-input>
                <br />
                <br />
              </el-radio>
              <br />
              <br />
              <el-radio label="2">
                B.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_b"
                ></el-input>
                <br />
                <br />
              </el-radio>
              <br />
              <br />
              <el-radio label="3">
                C.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_c"
                ></el-input>
                <br />
                <br />
              </el-radio>
              <br />
              <br />
              <el-radio label="4">
                D.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_d"
                ></el-input>
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>

        <div v-if="item.q_type === '2'">
          <el-form-item prop="resource">
            <p>请输入选项并选择正确答案</p>
            <el-checkbox-group v-model="item.checkList">
              <el-checkbox label="1">
                A.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_a"
                ></el-input>
              </el-checkbox>
              <br />
              <el-checkbox label="2">
                B.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_b"
                ></el-input>
              </el-checkbox>
              <br />
              <el-checkbox label="3">
                C.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_c"
                ></el-input>
              </el-checkbox>
              <br />
              <el-checkbox label="4">
                D.
                <el-input
                  placeholder="请输入题目描述"
                  v-model="item.option_d"
                ></el-input>
                <br />
              </el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </div>

        <div v-if="item.q_type === '3'">
          <el-form-item prop="resource">
            <p>请输入选项并选择正确答案</p>
            <el-radio-group v-model="item.answer">
              <el-radio label="1"> 正确 </el-radio>
              <br />
              <br />
              <el-radio label="2"> 错误 </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>
      </el-card>
    </div>
    <br />
    <el-button type="primary" @click="addQuestion">增加一题</el-button>
    <el-button type="primary" @click="save">保存</el-button>
  </el-form>
</template>

<script>
export default {
  name: "AddExam",
  data() {
    return {
      questionList: [
        {
          title: "",
          option_a: null,
          option_b: null,
          option_c: null,
          option_d: null,
          q_score: null,
          q_type: null,
          answer: null,
          checkList: [],
        },
      ],
      ruleForm: {
        resource: [],
        type: [],
      },
      course_id: "",
      ex_title: "",
      end_time: null,
      start_time: null,
    };
  },
  methods: {
    addQuestion() {
      var temp = {
        title: "",
        option_a: null,
        option_b: null,
        option_c: null,
        option_d: null,
        q_score: null,
        q_type: null,
        answer: null,
        checkList: [],
      };
      this.questionList.push(temp);
    },
    removeItem(index) {
      this.questionList.splice(index, 1);
    },
    addQue(exam_id) {
      for (var i = 0; i < this.questionList.length; i++) {
        if (this.questionList[i].answer != null)
          this.questionList[i].checkList.push(this.questionList[i].answer);
      }
      console.log(this.questionList);
      this.axios
        .post(
          "/api/addQuestion",
          JSON.stringify({
            exam_id: exam_id,
            questions: this.questionList,
          })
        )
        .then((res) => {
          if (res.data.code === 200) {
            this.$router.push({
              path: "/teacherHome/duty-course/exam/checkExam",
              query: {
                info: this.$Base64.encode(
                  JSON.stringify({ course_id: this.course_id })
                ),
              },
            });
          }
        });
    },
    save() {
      console.log("questionList", this.questionList);
      if (this.start_time === null) {
        this.$message("请选择起始时间");
        return;
      }
      if (this.end_time === null) {
        this.$message("请选择结束时间");
        return;
      }
      if (this.ex_title === null) {
        this.$message("请输入测试标题");
        return;
      }
      this.formatDateTime(this.end_time);
      this.axios
        .post(
          "/api/createExam",
          JSON.stringify({
            course_id: this.course_id,
            end_time: this.formatDateTime(this.end_time),
            start_time: this.formatDateTime(this.start_time),
            title: this.ex_title,
          })
        )
        .then((res) => {
          console.log("save()", res);
          if (res.data.code === 200) {
            this.addQue(res.data.data);
          }
        });
    },
    getParams() {
      this.course_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "course_id"
      ];
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
  },
  mounted() {
    this.getParams();
  },
};
</script>

<style>
.el-button--primary {
  color: white;
}
.el-button--success {
  color: white;
}
</style>

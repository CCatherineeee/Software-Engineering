<template>
  <div>
    <div>
      <div>
        <h2>{{ ex_title }}</h2>
        <br />
        <p><b>已进行</b> {{ time.timeStr }}</p>
        <br />
      </div>
      <el-form>
        <div v-for="(item, index) in questionList" :key="index">
          <el-card>
            <div>
              <!-- 题目的信息 -->
              <p style="font-weight: 700">
                第{{ index + 1 }}题 分值：{{ item.q_score }}
                <span v-if="item.q_type === 1">（单选）</span>
                <span v-if="item.q_type === 2">（多选）</span>
                <span v-if="item.q_type === 3">（判断）</span>
              </p>
              <br />
              <p>{{ item.title }}</p>

              <el-form-item v-if="item.q_type === 1">
                <el-radio-group v-model="answerList[index].answer">
                  <el-radio :label="1">A. {{ item.option_a }}</el-radio>
                  <el-radio :label="2">B. {{ item.option_b }}</el-radio>
                  <el-radio :label="3">C. {{ item.option_c }}</el-radio>
                  <el-radio :label="4">D. {{ item.option_d }}</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item v-if="item.q_type === 2">
                <el-checkbox-group v-model="answerList[index].checkList">
                  <el-checkbox :label="1"> A. {{ item.option_a }} </el-checkbox>
                  <br />
                  <el-checkbox :label="2"> B. {{ item.option_b }} </el-checkbox>
                  <br />
                  <el-checkbox :label="3"> C. {{ item.option_c }} </el-checkbox>
                  <br />
                  <el-checkbox :label="4">
                    D. {{ item.option_d }}
                    <br />
                  </el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item v-if="item.q_type === 3">
                <el-radio-group v-model="answerList[index].answer">
                  <el-radio :label="1">正确</el-radio>
                  <el-radio :label="2">错误</el-radio>
                </el-radio-group>
              </el-form-item>
            </div>
          </el-card>
        </div>
        <br />
        <el-button type="primary" @click="save">提交</el-button>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddExam",
  data() {
    return {
      questionList: [
        {
          title: "",
          option_a: "123",
          option_b: "123",
          option_c: "123",
          option_d: "123",

          q_score: 100,
          q_type: 1,
          answer: 0,
          q_id: null,
          checkList: null,
        },
      ],
      exam_id: "",
      ex_title: "",
      end_time: null,
      start_time: null,
      answerList: [],
      time: {
        hour: 0, //定义时，分，秒，毫秒并初始化为0；
        minute: 0,
        ms: 0,
        second: 0, //秒
        timeStr: "",
      },
      isClose: false,
      class_id: "",
      course_id: "",
    };
  },
  methods: {
    getParams() {
      this.exam_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "exam_id"
      ];
      this.course_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "course_id"
      ];
      console.log(this.class_id)
      this.class_id = this.course_id.substring(0, 12);
    },
    getExam() {
      this.axios
        .post(
          "/api/getExamById",
          JSON.stringify({
            exam_id: this.exam_id,
          })
        )
        .then((res) => {
          console.log(res);
          if (res.data.code === 200) {
            this.end_time = res.data.data.end_time;
            this.start_time = res.data.data.start_time;
            this.ex_title = res.data.data.ex_title;
            this.questionList = res.data.data.questions;
            for (let i = 0; i < res.data.data.questions.length; i++) {
              this.answerList.push({
                q_id: res.data.data.questions[i].q_id,
                answer: 0,
                checkList: [],
              });
            }
          }
        });
    },
    save() {
      for (let i = 0; i < this.answerList.length; i++) {
        if (this.answerList[i].answer !== 0) {
          this.answerList[i].checkList.push(this.answerList[i].answer);
        }
      }
      this.axios
        .post(
          "/api/submitExam",
          JSON.stringify({
            s_id: sessionStorage.getItem("id"),
            answerList: this.answerList,
          })
        )
        .then((res) => {
          if (res.data.code === 200) {
            this.$message("提交成功");
            this.$router.push({
              path: "/studentHome/concreteCourse/examHome/submit",
              query: {
                info: this.$Base64.encode(
                  JSON.stringify({ class_id: this.class_id, exam_id:this.exam_id,score:res.data.data.score, rank:res.data.data.rank })
                ),
              },
            });
          }
        });
    },
    formatDateTime(date) {
      //时间戳转换
      let y = date.getFullYear();
      let m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      let d = date.getDate();
      d = d < 10 ? "0" + d : d;
      let h = date.getHours();
      h = h < 10 ? "0" + h : h;
      let minute = date.getMinutes();
      minute = minute < 10 ? "0" + minute : minute;
      let second = date.getSeconds();
      second = second < 10 ? "0" + second : second;
      return y + "-" + m + "-" + d + " " + h + ":" + minute + ":" + second;
    },
    Timer() {
      this.time.timeStr = setInterval(this.timer, 50);
      setInterval(this.checkClose, 10);

    },
    timer() {
      //定义计时函数
      this.time.ms = this.time.ms + 50; //毫秒
      if (this.time.ms >= 1000) {
        this.time.ms = 0;
        this.time.second = this.time.second + 1; //秒
      }
      if (this.time.second >= 60) {
        this.time.second = 0;
        this.time.minute = this.time.minute + 1; //分钟
      }
      if (this.time.minute >= 60) {
        this.time.minute = 0;
        this.time.hour = this.time.hour + 1; //小时
      }
      this.time.timeStr =
        this.toDub(this.time.hour) +
        ":" +
        this.toDub(this.time.minute) +
        ":" +
        this.toDub(this.time.second); /*+""+this.toDubms(this.ms)+"毫秒"*/
      // document.getElementById('mytime').innerHTML=h+"时"+m+"分"+s+"秒"+ms+"毫秒";
    },
    toDub(n) {
      //补0操作
      if (n < 10) {
        return "0" + n;
      } else {
        return "" + n;
      }
    },
    checkClose() {
      if (this.isClose === true) return true;
      let yourtime = this.end_time.replace("-", "/");
      let d2 = new Date(); //取今天的日期
      let d1 = new Date(Date.parse(yourtime));
      if (d2 > d1) {
        this.isClose = true
        if(this.isClose){
          this.$message("考试关闭")
          this.save()
          return;
        }
      }
    },
  },
  mounted() {
    this.getParams();
    this.getExam();
    this.Timer();
  },
};
</script>

<style scoped>
</style>

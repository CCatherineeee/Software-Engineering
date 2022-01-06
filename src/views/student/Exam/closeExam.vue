<template>
  <div>
    <div>
      <div>
        <h2>{{ ex_title }}</h2>
        <br />
        <p>
          你的得分
          <el-tag>{{ score }} / {{ ex_score }}</el-tag>
        </p>
        <br />
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
              <el-row>
                <el-col :span="16">
                  <p>{{ item.title }}</p>
                </el-col>
                <el-col span="8">
                  <p>正确答案为：{{ correct[index] }}</p>
                </el-col>
              </el-row>

              <el-form-item
                v-if="item.q_type === 1"
                :class="getClass(index, item.q_type)"
              >
                <br />

                <el-radio-group disabled v-model="answerList[index].answer">
                  <el-radio label="1"
                    >A. {{ item.option_a }}
                    <br />
                    <br />
                  </el-radio>
                  <br />
                  <el-radio label="2"
                    >B. {{ item.option_b }}
                    <br />
                    <br />
                  </el-radio>
                  <br />
                  <el-radio label="3"
                    >C. {{ item.option_c }}
                    <br />
                    <br />
                  </el-radio>
                  <br />
                  <el-radio label="4"
                    >D. {{ item.option_d }}
                    <br />
                    <br />
                  </el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item
                v-if="item.q_type === 2"
                :class="getClass(index, item.q_type)"
              >
                <el-checkbox-group
                  v-model="answerList[index].checkList"
                  disabled
                >
                  <el-checkbox label="1" class="">
                    A. {{ item.option_a }}
                  </el-checkbox>
                  <br />
                  <el-checkbox label="2"> B. {{ item.option_b }} </el-checkbox>
                  <br />
                  <el-checkbox label="3"> C. {{ item.option_c }} </el-checkbox>
                  <br />
                  <el-checkbox label="4">
                    D. {{ item.option_d }}
                    <br />
                  </el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item
                v-if="item.q_type === 3"
                :class="getClass(index, item.q_type)"
              >
                <el-radio-group disabled v-model="answerList[index].answer">
                  <el-radio label="1">正确</el-radio>
                  <el-radio label="2">错误</el-radio>
                </el-radio-group>
              </el-form-item>
            </div>
          </el-card>
        </div>
        <br />
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "closeExam",
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
      correct: [],
      score: 0.0,
      ex_score: 0.0,
    };
  },
  methods: {
    getParams() {
      this.exam_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "exam_id"
      ];
    },
    getExam() {
      this.axios
        .post(
          "/api/getCloseExam",
          JSON.stringify({
            exam_id: this.exam_id,
            s_id: sessionStorage.getItem("id"),
          })
        )
        .then((res) => {
          if (res.data.code === 200) {
            this.score = res.data.data.score;
            this.end_time = res.data.data.end_time;
            this.start_time = res.data.data.start_time;
            this.ex_title = res.data.data.ex_title;
            this.ex_score = res.data.data.ex_score;
            this.questionList = res.data.data.questionList;
            if (res.data.data.answerList === null) this.answerList = [];
            else this.answerList = res.data.data.answerList;
            for (let i = 0; i < this.questionList.length; i++) {
              this.answerList.push({});
              if (
                this.questionList[i].q_type === 1 ||
                this.questionList[i].q_type === 3
              ) {
                var c = null;
                switch (this.questionList[i].answer) {
                  case 1 || "1":
                    c = "A";
                    break;
                  case 2 || "2":
                    c = "B";
                    break;
                  case 3 || "3":
                    c = "C";
                    break;
                  case 4 || "4":
                    c = "D";
                    break;
                }
                let temp = [];
                temp.push(c);
                this.correct.push(temp);
              } else {
                let t = [];
                for (
                  let j = 0;
                  j < this.questionList[i].checkList.length;
                  j++
                ) {
                  switch (this.questionList[i].checkList[j]) {
                    case 1:
                      c = "A";
                      break;
                    case 2:
                      c = "B";
                      break;
                    case 3:
                      c = "C";
                      break;
                    case 4:
                      c = "D";
                      break;
                  }
                  t.push(c);
                }
                this.correct.push(t);
              }
            }
            console.log(this.answerList);
            console.log(this.questionList);
          }
        });
    },
    getClass(index, type) {
      if (index > this.answerList.length) return "color-red";
      if (type === 1 || type === 3) {
        if (
          this.questionList[index].answer.toString() ===
          this.answerList[index].answer
        )
          return "color-green";
        else return "color-red";
      } else {
        if (
          this.questionList[index].checkList ===
          this.answerList[index].checkList
        )
          return "color-green";
        else return "color-red";
      }
    },
  },
  mounted() {
    this.getParams();
    this.getExam();
  },
};
</script>

<style scoped>
.color-warning {
  color: black;
}
.color-red {
  background-color: rgba(227, 209, 209, 0.2) !important;
}

.color-green {
  background-color: rgba(225, 241, 225, 0.99) !important;
}
</style>

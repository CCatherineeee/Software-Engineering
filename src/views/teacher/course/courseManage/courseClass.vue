<template>
  <div>
    <el-container>
      <el-aside width="40%">
        <el-row>
          <v-btn dark style="margin-bottom: 1%" @click="handleAddClass">
            新增班级
          </v-btn>
        </el-row>

        <v-row dense>
          <v-col v-for="item in classList" :key="item.class_id">
            <v-card color="#385F73" dark>
              <div>
                <v-card-title v-text="item.class_id"></v-card-title>
                <v-card-subtitle v-text="item.t_name"></v-card-subtitle>
                <v-card-actions>
                  <v-btn outlined rounded @click="handleTea(item)">
                    设置教师
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn text @click="handleDeleteClass(item)">
                    删除班级
                  </v-btn>
                </v-card-actions>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </el-aside>

      <el-main>
        <el-row>
          <el-col :span="5">
            <v-btn dark @click="handleAddEx">新增实验</v-btn></el-col
          >
          <el-col :span="7">
            <v-btn dark @click="handleScore">成绩占比</v-btn></el-col
          >
        </el-row>

        <el-row dense>
          <v-col v-for="item in experList" :key="item.ex_id">
            <v-card color="#1F7087" dark>
              <div>
                <v-card-title v-text="item.title"></v-card-title>
                <v-card-subtitle
                  v-text="'实验占比：' + item.weight"
                ></v-card-subtitle>
                <v-card-subtitle
                  v-if="item.status === 0"
                  v-text="'实验状态：未发布'"
                ></v-card-subtitle>
                <v-card-subtitle
                  v-if="item.status === 1"
                  v-text="'实验状态：已发布'"
                ></v-card-subtitle>
                <v-card-subtitle
                  v-if="item.status === 3"
                  v-text="'实验状态：已过期'"
                ></v-card-subtitle>
                <v-card-text
                  v-text="'截止日期：' + item.end_time"
                ></v-card-text>
                <v-card-actions>
                  <v-btn
                    text
                    @click="toExperiment(item)"
                    v-if="item.status !== 3"
                  >
                    详情
                  </v-btn>
                  <v-btn
                    text
                    @click="handleProportion(item)"
                    v-if="item.status !== 3"
                  >
                    占比
                  </v-btn>
                  <v-btn
                    text
                    @click="handlePushExper(item)"
                    v-if="item.status === 0"
                  >
                    发布
                  </v-btn>
                  <v-btn
                    text
                    @click="handleStopExper(item)"
                    v-if="item.status === 1"
                  >
                    终止
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn text @click="handleDeleteExper(item)"> 删除 </v-btn>
                </v-card-actions>
              </div>
            </v-card>
          </v-col>
        </el-row>

        <el-dialog
          :visible.sync="classDialog"
          title="新增班级"
          center
          width="300px"
        >
          <el-select v-model="tid">
            <el-option
              v-for="item in teaList"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            >
            </el-option>
          </el-select>

          <div slot="footer" class="dialog-footer">
            <el-button @click="classDialog = false">取消</el-button>
            <el-button type="primary" @click="createClass()">确定</el-button>
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="teaDialog"
          title="选择教师"
          center
          width="300px"
        >
          <el-select v-model="changeTemp.t_id">
            <el-option
              v-for="i in teaList"
              :key="i.id"
              :label="i.id"
              :value="i.id"
            >
            </el-option>
          </el-select>
          <div slot="footer" class="dialog-footer">
            <el-button @click="teaDialog = false">取消</el-button>
            <el-button type="primary" @click="updateTea(changeTemp)"
              >确定</el-button
            >
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="proDialog"
          title="设置实验占比"
          center
          width="300px"
        >
          <el-input v-model="changeTemp.weight"></el-input>
          <div slot="footer" class="dialog-footer">
            <el-button @click="proDialog = false">取消</el-button>
            <el-button type="primary" @click="setPro(changeTemp)"
              >确定</el-button
            >
          </div>
        </el-dialog>

        <el-dialog :visible.sync="exDialog" title="新增实验" center width="70%">
          <v-container>
            <v-row style="margin-bottom: 5px">
              <v-col cols="6">
                <el-date-picker
                  v-model="experiment.end_time"
                  type="datetime"
                  placeholder="选择实验截止日期时间"
                  :picker-options="pickerOptions"
                  style="margin-bottom: 15px; width: 100%"
                >
                </el-date-picker>
              </v-col>
              <v-col cols="6">
                <el-select
                  v-model="experiment.status"
                  placeholder="请选择实验提交方式"
                  style="margin-bottom: 15px; width: 100%"
                >
                  <el-option
                    v-for="item in exStatus"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </v-col>
              <v-col cols="6">
                <el-cascader
                  v-model="is_online"
                  placeholder="是否在线模拟"
                  :options="online_op"
                  @change="handleExChange"
                ></el-cascader>
              </v-col>
            </v-row>

            <v-textarea
              filled
              label="实验名称"
              auto-grow
              height="20px"
              v-model="experiment.title"
            ></v-textarea>

            <v-textarea
              filled
              label="实验简介"
              auto-grow
              v-model="experiment.brief"
            ></v-textarea>

            <v-textarea
              filled
              label="实验占比"
              auto-grow
              height="20px"
              v-model="experiment.weight"
            ></v-textarea>
          </v-container>

          <div slot="footer" class="dialog-footer">
            <el-button @click="exDialog = false">取消</el-button>
            <el-button type="primary" @click="addExSendMsg()">确定</el-button>
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="scoreDialog"
          title="设置成绩占比（以小数形式）"
          center
          width="50%"
        >
          <v-container>
            <v-textarea filled label="考试" auto-grow value=""></v-textarea>
            <el-input label="考试" v-model="eachScore.exam"></el-input>

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
      </el-main>
    </el-container>
  </div>
</template>

<script>
// import axios from 'axios';
export default {
  data() {
    return {
      syllabus: "",
      teaDialog: false,
      proDialog: false,
      fileDialog: false,
      classDialog: false,
      exDialog: false,
      scoreDialog: false,

      courseID: "",
      name: "",
      year: "",
      semester: "",
      id: "",
      is_online: "", //默认不是线上开课
      addSuccess: false,

      tid: "",
      teaList: [],
      classList: [],
      experList: [],
      fileList: [],
      stu_list: [],
      experiment: {
        courseID: "",
        title: "",
        brief: "",
        weight: "",
        end_time: "",
        status: null,
      },
      eachScore: {
        exam: "",
        report: "",
        attendance: "",
      },
      exStatus: [
        {
          value: "在线提交",
          label: "在线提交",
        },
        {
          value: "提交文件",
          label: "提交文件",
        },
      ],

      online_op: [
        {
          value: "0",
          label: "否",
        },
        {
          value: "1",
          label: "是",
          children: [
            {
              value: "paimai",
              label: "软件工程拍卖在线实验",
            },
          ],
        },
      ],

      changeTemp: {},
      timeout: null,
      pickerOptions: {
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            },
          },
          {
            text: "明天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24);
              picker.$emit("pick", date);
            },
          },
          {
            text: "一周后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            },
          },
        ],
      },
    };
  },
  methods: {
    handleExChange(value) {
      this.is_online = value[0];
      console.log(this.is_online);
    },
    getParams: function () {
      this.courseID = this.$route.query.c_id;
      this.name = this.$route.query.name;
      this.year = this.$route.query.year;
      this.semester = this.$route.query.semester;
      this.id = sessionStorage.getItem("id");
      this.experiment.courseID = this.$route.query.c_id;
    },
    handlePushExper(item) {
      this.axios
        .post(
          "/api/course/pushEx/",
          JSON.stringify({
            ex_id: item.ex_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("publish");
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.$message("发布成功！");
            this.getExperiment();
          }
        });
    },
    handleStopExper(item) {
      this.axios
        .post(
          "/api/course/stopEx/",
          JSON.stringify({
            ex_id: item.ex_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("publish");
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.$message("发布成功！");
            this.getExperiment();
          }
        });
    },
    handlePreview(file) {
      console.log(file);
    },

    handleRemove(file, fileListS) {
      console.log(file, fileListS);
    },

    handleChange(file) {
      console.log(file);
      this.fileListS.push(file);
      console.log(this.fileListS);
    },

    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    handleTea(item) {
      this.changeTemp = item;
      this.teaDialog = true;
    },
    handleProportion(item) {
      this.changeTemp = item;
      this.proDialog = true;
    },
    handleFile() {
      this.fileDialog = true;
    },
    handleAddClass() {
      this.classDialog = true;
    },
    handleAddEx() {
      this.experiment = {};
      this.exDialog = true;
    },
    handleScore() {
      this.scoreDialog = true;
    },
    handleDeleteClass(row) {
      this.$confirm("确认删除班级吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteClass(row);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          document.execCommand("Refresh");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },
    handleDeleteExper(item) {
      this.$confirm("确认删除实验吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteEx(item);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          document.execCommand("Refresh");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },

    updateTea(row) {
      var jsons = {
        class_id: row.class_id,
        t_id: row.t_id,
        token: sessionStorage.getItem("token"),
      };
      console.log("更新教师");
      console.log(jsons);
      this.axios
        .post("/api/manageClass/changeTeacher", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getClasses();
            this.teaDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setPro(row) {
      var jsons = {
        title: row.title,
        brief: row.brief,
        end_time: row.end_time,
        ex_id: row.ex_id,
        status: row.status,
        weight: row.weight,
        token: sessionStorage.getItem("token"),
      };
      console.log("更新占比");
      console.log(jsons);

      this.axios
        .post("/api/course/editEx/", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getExperiment();
            this.proDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      this.getExperiment();
    },
    toExperiment(row) {
      this.$router.push({
        path: "/teacherHome/manageExperiment",
        query: {
          info: this.$Base64.encode(JSON.stringify(row.ex_id)),
        },
      });
    },
    createClass() {
      this.axios
        .post(
          "/api/manageClass/addClass",
          JSON.stringify({
            courseID: this.courseID,
            t_id: this.tid,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.classDialog = false;
            this.tid = "";
            this.getClasses();
          }
        });
    },
    deleteClass(row) {
      var jsons = {
        classID: row.class_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/deleteClass", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getClasses();
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    classGetStudent() {
      //获取所有学生
      for (var i = 0; i < this.classList.length; i++) {
        var json3 = {
          class_id: this.classList[i]["class_id"],
        };
        console.log(this.classList[i]["class_id"]);
        return (
          this.axios
            //.post("/api/course/addEx/", JSON.stringify(jsons))
            .post("/api/manageClass/IDGetClassStudent", JSON.stringify(json3))
            .then((response) => {
              if (response.data["code"] === 400) {
                this.$message("班级不存在");
              } else {
                var class_student = response.data["data"];
                //求并集
                console.log(class_student);
                for (var t = 0; t < class_student.data.length; t++) {
                  this.stu_list.push(class_student.data[t]);
                }
              }
            })
        );
      }
    },
    async addExSendMsg() {
      await this.addEx();
      await this.classGetStudent();
      await this.sendStuMessage();
    },
    addEx() {
      this.addSuccess = false;

      var jsons = {
        courseID: this.courseID,
        title: this.experiment.title,
        brief: this.experiment.brief,
        weight: this.experiment.weight,
        end_time: this.formatDateTime(this.experiment.end_time),
        ex_type: this.experiment.status,
        token: sessionStorage.getItem("token"),
        is_online: this.is_online,
      };

      return (
        this.axios
          //.post("/api/course/addEx/", JSON.stringify(jsons))
          .post("/api/course/addEx/", JSON.stringify(jsons))
          .then((response) => {
            console.log("新增实验", response);
            if (response.data["code"] === 301) {
              this.$message("验证过期");
              this.$router.push({ path: "/login" });
            } else if (response.data["code"] === 404) {
              this.$message("找不到页面");
              this.$router.push({ path: "/404" });
            } else {
              if (response.data.data === "WeightUnreasonable") {
                this.$message("权重不合理！");
              } else {
                this.$message("添加成功！");
                this.addSuccess = true;
                this.exDialog = false;
                this.getExperiment();

                //这里给所有学生发信息,先获取所有班级
              }
            }
          })
      );
    },
    sendStuMessage() {
      //在这里添加，获取所有学生还要再写一个接口！！

      var end_time = this.experiment.end_time;
      console.log(end_time);
      if (this.addSuccess == true) {
        for (var i = 0; i < this.stu_list.length; i++) {
          var content =
            this.name +
            "已发布实验" +
            this.experiment.title +
            ",成绩占比" +
            this.experiment.weight +
            ",请在" +
            this.formatDateTime(this.experiment.end_time) +
            "前完成";
          var json4 = {
            s_id: this.stu_list[i]["s_id"],
            title: "实验——" + this.experiment.title + "已新增",
            content: content,
            deadline: this.formatDateTime(this.experiment.end_time),
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
    deleteEx(item) {
      var jsons = {
        ex_id: item.ex_id,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/course/delEx/", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getExperiment();
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    getClasses() {
      var jsons = {
        courseID: this.courseID,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/manageClass/showClass/", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.classList = response.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });

      /*this.axios({
        method: "get",
        url: "/api/showClass/",
        crossDomain: true,
        data: JSON.stringify(jsons),
      })
        .then((response) => {
          console.log(response);
          // this.classList = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });*/
    },
    getExperiment() {
      var jsons = {
        c_id: this.courseID,
        token: sessionStorage.getItem("token"),
      };
      this.axios
        .post("/api/course/getEx/", JSON.stringify(jsons))
        .then((response) => {
          console.log("exList");
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.experList = response.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getTeaList() {
      //获得所有教师
      this.axios
        .get("/api/course/getAllTeacher/", {
          params: { token: sessionStorage.getItem("token") },
          crossDomain: true,
        })
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.teaList = response.data.data;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setScore() {
      //设置成绩占比
      var exam = this.eachScore.exam * 1;
      var report = this.eachScore.report * 1;
      var attendance = this.eachScore.attendance * 1;
      if (exam + report + attendance != 1)
        this.$message.warning("所有成绩加合不为1，请重新输入！");
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
    this.getClasses();
    this.getExperiment();
    this.getTeaList();
  },
};
</script>

<style scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
  overflow-y: hidden;
}
.el-button--primary {
  color: white;
}
</style>

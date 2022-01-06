<template>
  <div>
    <el-tabs v-model="activeName">
      <el-tab-pane label="详情" name="first">
        <el-container style="margin-left: 5%; margin-right: 5%; margin-top: 3%">
          <el-main>
            <v-row style="margin-bottom: 10px">
              <v-col cols="6">
                <el-date-picker
                  type="datetime"
                  placeholder="截止时间"
                  :disabled="readOnly"
                  :picker-options="pickerOptions"
                  v-model="ex_info.end_time"
                  style="width: 100%"
                ></el-date-picker>
              </v-col>
              <v-col cols="6">
                <el-select
                  :disabled="readOnly"
                  v-model="ex_info.ex_type"
                  placeholder="提交方式"
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
            </v-row>

            <v-textarea
              :disabled="readOnly"
              filled
              label="实验名称"
              auto-grow
              height="20px"
              v-model="ex_info.title"
              :value="ex_info.title"
            ></v-textarea>

            <v-textarea
              filled
              :disabled="readOnly"
              label="实验权重"
              height="20px"
              auto-grow
              v-model="ex_info.weight"
              :value="ex_info.weight"
            ></v-textarea>

            <v-textarea
              filled
              :disabled="readOnly"
              label="实验简介"
              auto-grow
              v-model="ex_info.brief"
              :value="ex_info.brief"
            ></v-textarea>

            <v-row style="margin-bottom: 10px">
              <v-col cols="1"><v-btn dark @click="back">返回</v-btn></v-col>
              <v-col cols="1"
                ><v-btn
                  dark
                  @click="editExper"
                  v-if="ex_info.status == '未发布'"
                  >确定</v-btn
                ></v-col
              >
            </v-row>
          </el-main>
        </el-container></el-tab-pane
      >

      <el-tab-pane label="实验指导" name="second">
        <el-container style="margin-left: 5%; margin-right: 5%; margin-top: 3%">
          <el-main>
            <v-textarea
              filled
              label="实验目的"
              auto-grow
              :value="purpose"
            ></v-textarea>

            <v-textarea
              filled
              label="实验设备"
              auto-grow
              :value="equipment"
            ></v-textarea>

            <v-textarea
              filled
              label="实验步骤"
              auto-grow
              :value="step"
            ></v-textarea>

            <v-textarea
              filled
              label="实验过程"
              auto-grow
              :value="process"
            ></v-textarea>

            <v-textarea
              filled
              label="结果分析"
              auto-grow
              :value="result"
            ></v-textarea>
            <v-row style="margin-bottom: 10px">
              <v-col cols="1"><v-btn dark @click="back">返回</v-btn></v-col>
              <v-col cols="1"
                ><v-btn
                  dark
                  @click="editExper"
                  v-if="ex_info.status == '未发布'"
                  >确定</v-btn
                ></v-col
              >
            </v-row>
          </el-main>
        </el-container></el-tab-pane
      >
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      ex_id: "",
      ex_info: {},
      readOnly: true,
      activeName: "first",
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

      purpose: "目的",
      equipment: "设备",
      step: "步骤",
      process: "过程",
      result: "结果",
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
    getParams: function () {
      this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info));
    },
    back() {
      this.$router.go(-1);
    },
    getExInfo() {
      var jsons = {
        ex_id: this.ex_id,
      };
      this.axios
        .post("/api/course/getExById/", JSON.stringify(jsons))
        .then((response) => {
          //这里使用了ES6的语法
          //this.tableData = response.data
          console.log("getExInfo");
          console.log(response);
          if (response.data.data.status == 0) {
            response.data.data.status = "未发布";
            this.readOnly = false;
          }
          if (response.data.data.status == 1)
            response.data.data.status = "未截止";
          if (response.data.data.status == 3)
            response.data.data.status = "已截止";
          this.ex_info = response.data.data;
        });
    },
    editExper() {
      //修改实验信息
      var jsons = {
        title: this.ex_info.title,
        brief: this.ex_info.brief,
        end_time:this.ex_info.end_time,
        ex_id: this.ex_info.ex_id,
        status: this.ex_info.status,
        weight: this.ex_info.weight,
        token: sessionStorage.getItem("token"),
      };

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
            this.$message("修改成功");
            this.$router.go(0);
            this.proDialog = false;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  mounted() {
    this.getParams();
    this.getExInfo();
  },
};
</script>

<style scoped>
.box-card {
  border-radius: 15px;
  box-shadow: 7px 7px 10px rgba(0, 0, 0, 0.15);
}
.el-card {
  margin-bottom: 20px;
  margin-top: 15px;
}
.el-button--primary {
  color: white;
}
</style>
<template>
  <div>
    <h3
      style="
        display: flex;
        align-items: center;
        color: #ef5350;
        margin-bottom: 5px;
      "
    >
      各项占总成绩比例： 实验:50% ；测验:40% ；出勤:10%
    </h3>

    <v-card style="display: flex; justify-content: center; margin-bottom: 5px">
      <div
        id="myChart"
        style="width: 800px; height: 500px; display: flex; align-items: center"
      />
      <h3 style="display: flex; align-items: center">
        所得成绩占比:{{ now_score }}/100
      </h3>
    </v-card>

    <v-card style="display: flex; justify-content: center; margin-bottom: 5px">
      <v-card-title>
        <h3 style="color: #6666cc">详细出勤情况:100</h3>
      </v-card-title>

      <el-row>
        <el-row>
          <el-col :span="24">
            <el-table
              :data="
                tableData.slice(
                  (currentPageA - 1) * pagesize,
                  currentPageA * pagesize
                )
              "
              :stripe="true"
              style="width: 100%; margin-left: 7%; margin-right: 10%"
            >
              <el-table-column prop="date" label="序号" width="180">
              </el-table-column>
              <el-table-column prop="name" label="实验" width="180" />

              <el-table-column
                prop="name"
                label="是否提交"
              /> </el-table></el-col
        ></el-row>
        <el-row>
          <el-col :span="24">
            <el-pagination
              @current-change="handleCurrentChangeA"
              :current-page="currentPageA"
              :page-size="pagesize"
              layout="total, prev, pager, next, jumper"
              :total="tableData.length"
            >
            </el-pagination></el-col></el-row
      ></el-row>
    </v-card>
    <v-card style="display: flex; justify-content: center; margin-bottom: 5px">
      <v-card-title>
        <h3 style="color: #6666cc">报告得分与权重:100</h3>
      </v-card-title>

      <el-row>
        <el-row>
          <el-col :span="24">
            <el-table
              :data="
                tableData.slice(
                  (currentPageR - 1) * pagesize,
                  currentPageR * pagesize
                )
              "
              :stripe="true"
              style="width: 100%; margin-left: 7%; margin-right: 10%"
            >
              <el-table-column prop="date" label="序号" width="180">
              </el-table-column>
              <el-table-column prop="name" label="实验" width="180" />
              <el-table-column prop="name" label="权重" width="180" />

              <el-table-column prop="name" label="得分" /> </el-table></el-col
        ></el-row>
        <el-row>
          <el-col :span="24">
            <el-pagination
              @current-change="handleCurrentChangeR"
              :current-page="currentPageR"
              :page-size="pagesize"
              layout="total, prev, pager, next, jumper"
              :total="tableData.length"
            >
            </el-pagination></el-col></el-row
      ></el-row>
    </v-card>
    <v-card style="display: flex; justify-content: center; margin-bottom: 5px">
      <v-card-title>
        <h3 style="color: #6666cc">测验得分:100</h3>
      </v-card-title>

      <el-row>
        <el-row>
          <el-col :span="24">
            <el-table
              :data="
                tableData.slice(
                  (currentPageE - 1) * pagesize,
                  currentPageE * pagesize
                )
              "
              :stripe="true"
              style="width: 100%; margin-left: 7%; margin-right: 10%"
            >
              <el-table-column prop="date" label="序号" width="180">
              </el-table-column>
              <el-table-column prop="name" label="测验" width="180" />
              <el-table-column prop="name" label="总分" width="180" />

              <el-table-column prop="name" label="得分" /> </el-table></el-col
        ></el-row>
        <el-row>
          <el-col :span="24">
            <el-pagination
              @current-change="handleCurrentChangeE"
              :current-page="currentPageE"
              :page-size="pagesize"
              layout="total, prev, pager, next, jumper"
              :total="tableData.length"
            >
            </el-pagination></el-col></el-row></el-row
    ></v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPageA: 1,
      currentPageR: 1,
      currentPageE: 1,
      pagesize: 6,
      allScore: [],
      class_id: null,
      now_score: 0,
      tableData: [
        {
          date: "2016-05-02",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1518 弄",
        },
        {
          date: "2016-05-04",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1517 弄",
        },
        {
          date: "2016-05-01",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1519 弄",
        },
        {
          date: "2016-05-03",
          name: "王小虎",
          address: "上海市普陀区金沙江路 1516 弄",
        },
      ],
    };
  },
  methods: {
    handleCurrentChangeA: function (currentPage) {
      this.currentPageA = currentPage;
    },

    handleCurrentChangeR: function (currentPage) {
      this.currentPageR = currentPage;
    },

    handleCurrentChangeE: function (currentPage) {
      this.currentPageE = currentPage;
    },
    getParams: function () {
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
    },
    getAllScore() {
      var json = {
        class_id: this.class_id,
        s_id: sessionStorage.getItem("id"),
      };
      this.axios
        .post("/api/Ex/getClassAllScore", JSON.stringify(json))
        .then((response) => {
          console.log("getAllScore", response);

          var data = response.data["data"];
          this.allScore = data;
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    exChart() {
      var echarts = require("echarts");
      let myChart = echarts.init(document.getElementById("myChart"));
      myChart.clear();
      var option = {
        backgroundColor: "#FFFFFF",

        title: {
          text: "您的成绩",
          left: "center",
          top: 20,
          textStyle: {
            color: "#3366CC",
          },
        },

        tooltip: {
          trigger: "item",
        },

        series: [
          {
            name: "实验名称",
            type: "pie",
            radius: "55%",
            center: ["50%", "50%"],
            data: this.allScore.sort(function (a, b) {
              return a.value - b.value;
            }),
            label: {
              color: "#000000",
            },
            labelLine: {
              lineStyle: {
                color: "#000000",
              },
              smooth: 0.2,
              length: 10,
              length2: 20,
            },
            itemStyle: {
              shadowBlur: 300,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },

            animationType: "scale",
            animationEasing: "elasticOut",
            animationDelay: function () {
              return Math.random() * 200;
            },
          },
        ],
      };
      myChart.setOption(option);
      myChart.resize();
    },
    /*examChart() {
      var echarts = require("echarts");
      let myChart = echarts.init(document.getElementById("examChart"));
      myChart.clear();
      var option = {
        backgroundColor: "#FFFFFF",

        title: {
          text: "测验成绩",
          left: "center",
          top: 20,
          textStyle: {
            color: "#3366CC",
          },
        },

        tooltip: {
          trigger: "item",
        },

        series: [
          {
            name: "测验名称",
            type: "pie",
            radius: "55%",
            center: ["50%", "50%"],
            data: this.allScore.sort(function (a, b) {
              return a.value - b.value;
            }),
            label: {
              color: "#000000",
            },
            labelLine: {
              lineStyle: {
                color: "#000000",
              },
              smooth: 0.2,
              length: 10,
              length2: 20,
            },
            itemStyle: {
              normal: {
                color: function (colors) {
                  var colorList = [
                    "#003300",
                    "#6666CC",
                    "#336699",
                    "#666699",
                    "#663366",
                    "#666666",
                    "#999966",
                    "#993333",
                    "#CC3333",
                    "#CC99CC",
                    "#CCCC99",
                    "#663333",
                  ];
                  return colorList[colors.dataIndex];
                },
              },
              shadowBlur: 300,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },

            animationType: "scale",
            animationEasing: "elasticOut",
            animationDelay: function () {
              return Math.random() * 200;
            },
          },
        ],
      };
      myChart.setOption(option);
      myChart.resize();
    },
    scoreChart() {
      var echarts = require("echarts");
      let myChart = echarts.init(document.getElementById("scoreChart"));
      myChart.clear();
      var option = {
        backgroundColor: "#FFFFFF",

        title: {
          text: "总成绩",
          left: "center",
          top: 20,
          textStyle: {
            color: "#3366CC",
          },
        },

        tooltip: {
          trigger: "item",
        },

        series: [
          {
            type: "pie",
            radius: "55%",
            center: ["50%", "50%"],
            data: this.allScore.sort(function (a, b) {
              return a.value - b.value;
            }),
            label: {
              color: "#000000",
            },
            labelLine: {
              lineStyle: {
                color: "#000000",
              },
              smooth: 0.2,
              length: 10,
              length2: 20,
            },
            itemStyle: {
              normal: {
                color: function (colors) {
                  var colorList = [
                    "#663366",
                    "#666666",
                    "#999966",
                    "#993333",
                    "#CC3333",
                    "#CC99CC",
                    "#CCCC99",
                    "#663333",
                    "#003300",
                    "#6666CC",
                    "#336699",
                    "#666699",
                  ];
                  return colorList[colors.dataIndex];
                },
              },
              shadowBlur: 300,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },

            animationType: "scale",
            animationEasing: "elasticOut",
            animationDelay: function () {
              return Math.random() * 200;
            },
          },
        ],
      };
      myChart.setOption(option);
      myChart.resize();
    },*/
    getNowScore() {
      for (var i = 0; i < this.allScore.length; i++) {
        this.now_score += this.allScore[i].value;
      }
      this.now_score = this.now_score.toFixed(2);
    },
  },
  mounted() {
    this.getParams();
    this.getAllScore();
    setTimeout(() => {
      this.exChart();
    }, 760);
    /* setTimeout(() => {
      this.examChart();
    }, 760);
    setTimeout(() => {
      this.scoreChart();
    }, 760);*/
    setTimeout(() => {
      this.getNowScore();
    }, 760);
  },
};
</script>
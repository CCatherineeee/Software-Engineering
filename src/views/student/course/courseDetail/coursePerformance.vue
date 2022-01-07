<template>
  <div>
    <v-card style="display: flex; justify-content: center">
      <div id="scoreChart" style="width: 800px; height: 500px" />
      <h3 style="display: flex; align-items: center">
        所得成绩占比:{{ now_score }}/100
      </h3>
    </v-card>
    <v-card style="display: flex; justify-content: center">
      <div id="myChart" style="width: 800px; height: 500px" />
      <h3 style="display: flex; align-items: center">
        所得成绩占比:{{ now_score }}/100
      </h3>
    </v-card>
    <v-card style="display: flex; justify-content: center">
      <div id="examChart" style="width: 800px; height: 500px" />
      <h3 style="display: flex; align-items: center">
        所得成绩占比:{{ now_score }}/100
      </h3>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allScore: [],
      class_id: null,
      now_score: 0,
    };
  },
  methods: {
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
          text: "实验成绩",
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
    examChart() {
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
    },
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
    setTimeout(() => {
      this.examChart();
    }, 760);
    setTimeout(() => {
      this.scoreChart();
    }, 760);
    setTimeout(() => {
      this.getNowScore();
    }, 760);
  },
};
</script>
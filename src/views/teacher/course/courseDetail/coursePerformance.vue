<template>
  <div>
    <div ref="experiment" style="width: 100%; height: 400px"></div>
  </div>
</template>


<script>
//import echarts from "echarts";
export default {
  data() {
    return {
      id: "",
      c_id: "",

      experimentName: [],

      excellentList: [],
      goodList: [],
      middleList: [],
      passList: [],
      noPassList: [],
    };
  },
  methods: {
    getCourseScore() {
      var classID = this.c_id.toString();
      console.log("cid==" + classID);
      this.axios
        .post(
          "/api/tea/score",
          JSON.stringify({
            class_id: classID,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          //这里使用了ES6的语法
          console.log("getCourseScore", response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.experimentScore = response.data;
            this.experimentName = response.data.name;
            //console.log("this.option.xAxis.data",this.option.xAxis.data);
            for (var j = 0; j < response.data.count.length; j++) {
              this.excellentList.push(response.data.count[j][0]);
            }
            for (var q = 0; q < response.data.count.length; q++) {
              this.goodList.push(response.data.count[q][1]);
            }
            for (var w = 0; w < response.data.count.length; w++) {
              this.middleList.push(response.data.count[w][2]);
            }
            for (var e = 0; e < response.data.count.length; e++) {
              this.passList.push(response.data.count[e][3]);
            }
            for (var r = 0; r < response.data.count.length; r++) {
              this.noPassList.push(response.data.count[r][4]);
            }
            console.log("优", this.excellentList);
            console.log("良", this.goodList);
            console.log("中", this.middleList);
            console.log("及格", this.passList);
            console.log("不及格", this.noPassList);

            this.drawLine();
          }
        });
    },

    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      var echarts = require("echarts");
      let myChart = echarts.init(this.$refs.experiment);
      // 绘制图表
      let option = {
        xAxis: {
          type: "category",
          data: this.experimentName,
          name: "实验", //x坐标轴的名称
        },
        yAxis: {
          type: "value",
          name: "人数", //x坐标轴的名称
        },
        series: [
          {
            data: this.excellentList,
            type: "bar",
            name: "优", //柱状条顶部标签内容（配合label使用），也可显示为气泡提示的y轴数据字段名
            showBackground: true,
            backgroundStyle: {
              color: "rgba(220, 220, 220, 0.8)",
            },
            // 柱状条顶部标签内容设置，笔者此处不需要此设置，因此将示例代码注释掉了
            label: {
              show: true,
              position: "center",
              color: "#fff",
            },
          },
          {
            data: this.goodList,
            type: "bar",
            name: "良", //柱状条顶部标签内容（配合label使用），也可显示为气泡提示的y轴数据字段名
            showBackground: true,
            backgroundStyle: {
              color: "rgba(220, 220, 220, 0.8)",
            },
            label: {
              show: true,
              position: "center",
              color: "#fff",
            },
          },
          {
            data: this.middleList,
            type: "bar",
            name: "中", //柱状条顶部标签内容（配合label使用），也可显示为气泡提示的y轴数据字段名
            showBackground: true,
            backgroundStyle: {
              color: "rgba(220, 220, 220, 0.8)",
            },
            label: {
              show: true,
              position: "center",
              color: "#fff",
            },
          },
          {
            data: this.passList,
            type: "bar",
            name: "及格", //柱状条顶部标签内容（配合label使用），也可显示为气泡提示的y轴数据字段名
            showBackground: true,
            backgroundStyle: {
              color: "rgba(220, 220, 220, 0.8)",
            },
            label: {
              show: true,
              position: "center",
              color: "#fff",
            },
          },
          {
            data: this.noPassList,
            type: "bar",
            name: "不及格", //柱状条顶部标签内容（配合label使用），也可显示为气泡提示的y轴数据字段名
            showBackground: true,
            backgroundStyle: {
              color: "rgba(220, 220, 220, 0.8)",
            },
            label: {
              show: true,
              position: "center",
              color: "#fff",
            },
          },
        ],
        tooltip: {
          trigger: "axis", // 触发类型，'item'-数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用，'axis'- 坐标轴触发，主要在柱状图，折线图等会使用类目轴的图表中使用
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow", // 鼠标移动到数据上出现的样式控制 默认为直线，可选为：'line' | 'shadow'
            shadowStyle: {
              // 阴影样式  若选择 type 为 line的类型，可设置线条样式 lineStyle
              color: "rgba(88,101,137,0.3)",
              width: "auto",
              type: "default",
            },
          },
        },
        legend: {
          data: ["优", "良", "中", "及格", "不及格"],
          top: 10,
        },
      };
      //let option = this.option;

      myChart.setOption(option);
    },

    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
    },
  },
  mounted() {
    this.getParams();
    this.getCourseScore();
    //this.drawLine();
  },
};
</script>

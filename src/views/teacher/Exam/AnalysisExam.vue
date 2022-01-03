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

      option: {
        xAxis: {
          type: "value",
          name: "人数", //x坐标轴的名称
        },
        yAxis: {
          type: "category",
          data: ["Mon"],
          name: "实验", //x坐标轴的名称
        },
        series: [
          {
            data: [120, 200],
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
            data: [120, 200],
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
          data: ["优", "良", "中"],
          top: 10,
        },
      },
    };
  },
  methods: {
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      var echarts = require("echarts");
      let myChart = echarts.init(this.$refs.experiment);
      // 绘制图表
      let option = this.option;

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

    this.drawLine();
  },
};
</script>

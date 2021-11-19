<template>
  <div>
    <p style="margin: 10px auto 10px auto; font: 20px Microsoft YaHei">
      效果展示
    </p>
    <div id="exportPdf" ref="exportPdf">
      <el-card style="margin-bottom: 20px">
        <el-descriptions
          direction="vertical"
          :column="1"
          border
          size="medium"
          style="
            margin-top: 20px;
            margin-right: 50px;
            margin-left: 50px;
            margin-bottom: 20px;
          "
        >
          <el-descriptions-item label="截止日期"
            >{{ date1 }} —— {{ date2 }}</el-descriptions-item
          >
          <el-descriptions-item label="实验名称">{{
            name
          }}</el-descriptions-item>
          <el-descriptions-item label="实验目的">{{
            purpose
          }}</el-descriptions-item>
          <el-descriptions-item label="实验设备" :span="2">{{
            equipment
          }}</el-descriptions-item>

          <el-descriptions-item label="实验步骤">{{
            step
          }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>

    <el-row :gutter="10">
      <el-col :span="3" :offset="9"
        ><v-btn dark @click="publish">发布</v-btn></el-col
      >
      <el-col :span="3"><v-btn dark @click="back">取消</v-btn></el-col>
    </el-row>
  </div>
</template>
    
<script>
export default {
  data() {
    return {
      date1: "",
      date2: "",
      name: "",
      purpose: "",
      equipment: "",
      step: "",
      process: "",
      result: "",
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      // 将数据放在当前组件的数据内
      console.log("传来的参数==" + this.$route.query.date1);
      (this.date1 = this.$route.query.date1),
        (this.date2 = this.$route.query.date2),
        (this.name = this.$route.query.name),
        (this.purpose = this.$route.query.purpose),
        (this.equipment = this.$route.query.equipment),
        (this.step = this.$route.query.step),
        (this.process = this.$route.query.process),
        (this.result = this.$route.query.result);
    },

    publish() {
      //this.isSeen = true;
      this.$PDFSave(this.$refs.exportPdf, "我的文件");
      //this.isSeen = false;
      //this.doPrint3();
    },

    back() {
      this.$router.push("/teacherHome/concreteCourse/addExper");
    },

    doPrint3() {
      //判断iframe是否存在，不存在则创建iframe
      var iframe = document.getElementById("print-iframe");
      if (!iframe) {
        var el = document.getElementById("exportPdf");
        iframe = document.createElement("IFRAME");
        var doc = null;
        iframe.setAttribute("id", "print-iframe");
        iframe.setAttribute(
          "style",
          "position:absolute;width:0px;height:0px;left:-500px;top:-500px;"
        );
        document.body.appendChild(iframe);
        doc = iframe.contentWindow.document;
        //这里可以自定义样式
        doc.write(
          '<style media="print">@page {size: auto;margin: 0mm;}</style>'
        ); //解决出现页眉页脚和路径的问题
        doc.write("<div>" + el.innerHTML + "</div>");
        doc.close();
        iframe.contentWindow.focus();
      }
      setTimeout(function () {
        iframe.contentWindow.print();
      }, 50); //解决第一次样式不生效的问题
      if (navigator.userAgent.indexOf("MSIE") > 0) {
        document.body.removeChild(iframe);
      }
    },
  },
  mounted() {
    this.getParams();
  },
};
</script>
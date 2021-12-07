<template>
  <div>
    <v-container>
      <v-row style="margin-bottom: 10px">
        <v-col cols="6">
          <el-date-picker
            type="date"
            placeholder="截止日期"
            v-model="date1"
            style="width: 100%"
          ></el-date-picker>
        </v-col>
        <v-col cols="6">
          <el-time-picker
            placeholder="截止时间"
            v-model="date2"
            style="width: 100%"
          ></el-time-picker>
        </v-col>
      </v-row>

      <v-textarea
        filled
        label="实验名称"
        auto-grow
        height="20px"
        :value="name"
      ></v-textarea>

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

      <v-textarea filled label="实验步骤" auto-grow :value="step"></v-textarea>

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
      <el-row :gutter="10">
        <el-col :span="3" :offset="9"
          ><v-btn dark @click="publish">发布</v-btn></el-col
        >
        <el-col :span="3"><v-btn dark @click="confirm">确定</v-btn></el-col>
        <el-col :span="3"><v-btn dark @click="back">取消</v-btn></el-col>
        <el-col :span="3"><v-btn dark @click="check">测试</v-btn></el-col>
      </el-row>
    </v-container>

    <div id="exportPdf" ref="exportPdf" v-show="isSeen">
      <el-card>
        <el-descriptions
          direction="vertical"
          :column="1"
          border
          size="medium"
          style="margin-top: 20px; margin-right: 50px; margin-left: 50px"
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      isSeen: false,
      id: "",
      date1: "2015-1-1",
      date2: "00:00:00",
      name: "名称",
      purpose: "目的",
      equipment: "设备",
      step: "步骤",
      process: "过程",
      result: "结果",
    };
  },
  methods: {
    getParams: function () {
      // 取到路由带过来的参数
      var routerParams = this.$route.query.id;
      // 将数据放在当前组件的数据内
      console.log("传来的参数==" + routerParams);
      this.id = routerParams;
    },

    publish() {
      //this.isSeen = true;
      this.$PDFSave(this.$refs.exportPdf, "我的文件");
      //this.isSeen = false;
      //this.doPrint3();
      //this.getPdf();
    },

    confirm() {
      this.$router.push({
        path: "/teacherHome/concreteCourse/PreviewExper",
        query: {
          date1: this.date1,
          date2: this.date2,
          name: this.name,
          purpose: this.purpose,
          equipment: this.equipment,
          step: this.step,
          process: this.process,
          result: this.result,
        },
      });
      //this.$router.push("/teacherHome/concreteCourse/PreviewExper");
    },

    back() {
      this.$router.push("/teacherHome/concreteCourse/Exper");
    },

    doPrint3() {
      //判断iframe是否存在，不存在则创建iframe
      //调用win.print（）
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

    getExper() {
      //获得试验信息
      this.axios
        .get("", {
          params: { id: this.id },
          crossDomain: true,
        })
        .then((response) => {
          console.log(response);

          //this.role = response.data[0].role;
          //this.department = response.data[0].department;
          //this.major_id;
        })
        .catch(function (error) {
          console(error);
        });
    },
    check() {
      console.log(this.date1);
      console.log(this.date2);
    },
  },
  mounted() {
    this.getParams();
    this.getExper();
  },
};
</script>
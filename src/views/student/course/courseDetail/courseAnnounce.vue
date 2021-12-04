<template>
  <div>
    <el-timeline>
      <el-timeline-item
        v-for="(data, index) in dataTable"
        :key="index"
        placement="top"
        :timestamp="data.date"
      >
        <el-card
          style="box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15); margin-right: 20%"
        >
          <h2>{{ data.title }}</h2>
          <el-link @click="handleTitle(data)">{{ data.content }}</el-link>
          <p style="text-align: right">{{ data.name }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
    <el-dialog :visible.sync="dialogVisible" :title="this.title" center>
      <span class="dialogBack">{{ this.content }}</span>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"
          >确定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "",
      content: "",
      dialogVisible: false,
      dataTable: [],
      class_id : ""
    };
  },
  methods: {
    handleTitle(data) {
      this.title = data.title;
      this.content = data.content;
      this.dialogVisible = true;
    },
  },
  mounted() {
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id']
    this.axios.post(
        "/api/course/getAnn/",JSON.stringify(
            {
              class_id : this.class_id,
            }),
    ).then((response) => {
      //这里使用了ES6的语法
      this.dataTable = response.data
      //this.checkResponse(response.data); //请求成功返回的数据
    })
  }
};
</script>
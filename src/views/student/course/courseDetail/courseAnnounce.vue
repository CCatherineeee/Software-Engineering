<template>
  <div>
    <el-timeline>
      <el-timeline-item
        v-for="data in annList"
        :key="data.ann_id"
        placement="top"
        :timestamp="data.date"
      >
        <el-card
          style="box-shadow: 7px 7px 7px rgba(0, 0, 0, 0.15); margin-right: 20%"
        >
          <h2>{{ data.title }}</h2>
          <el-link @click="handleTitle(data)"
            ><p v-html="data.content"></p
          ></el-link>
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
      annList: [],
      class_id: "",
    };
  },
  methods: {
    handleTitle(data) {
      this.title = data.title;
      this.content = data.content;
      this.dialogVisible = true;
    },
    getAnnList() {
      this.axios
        .post(
          "/api/course/getAnn/",
          JSON.stringify({
            class_id: this.class_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log(response.data["data"]);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            //这里使用了ES6的语法
            this.annList = response.data.data;
            console.log(this.annList);
          }
        });
    },
    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      console.log("cid===" + this.class_id);
    },
  },
  mounted() {
    this.getParams();
    this.getAnnList();
  },
};
</script>
<style>
.el-button--primary {
  color: white;
}
</style>
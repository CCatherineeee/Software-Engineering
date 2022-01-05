<template>
  <div>
    <el-container style="margin-top: 20px">
      <el-main>
        <v-btn
          color="orange lighten-2"
          dark
          @click="handleAnn"
          style="margin-bottom: 20px"
        >
          新增公告
        </v-btn>
        <el-timeline>
          <el-timeline-item
            v-for="data in annList"
            :key="data.ann_id"
            center
            placement="top"
            :timestamp="data.date"
          >
            <el-card>
              <el-link @click="handleTitle(data)">
                <h2>{{ data.title }}</h2></el-link
              >

              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                size="mini"
                style="float: right; margin-left: 5px"
                @click="handleDelete(data)"
              ></el-button>

              <el-button
                type="primary"
                icon="el-icon-zoom-in"
                circle
                size="mini"
                style="float: right"
                @click="handleTitle(data)"
              ></el-button>
            </el-card>
          </el-timeline-item>
        </el-timeline>

        <el-dialog :visible.sync="dialogVisible" :title="this.title" center>
          <v-textarea filled auto-grow :value="content" disabled></v-textarea>
          <div slot="footer">
            <el-button type="primary" @click="dialogVisible = false"
              >确定</el-button
            >
          </div>
        </el-dialog>
        <el-dialog :visible.sync="dialogAddVisible" title="新增公告" center>
          <el-form
            :model="formAnn"
            style="margin: 40px 65px 0px 25px"
            label-width="80px"
          >
            <el-form-item
              label="标题"
              :required="true"
              prop="title"
              status-icon="true"
            >
              <el-input v-model="formAnn.title" autocomplete="off"></el-input>
            </el-form-item>

            <el-form-item
              label="内容"
              :required="true"
              prop="content"
              status-icon="true"
            >
              <el-input v-model="formAnn.content" type="textarea"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer">
            <el-button @click="dialogAddVisible = false">取消</el-button>
            <el-button type="primary" @click="addAnn()">确定</el-button>
          </div>
        </el-dialog>
      </el-main>
      <el-aside></el-aside>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: "",
      c_id: "",
      title: "",
      content: "",
      contentRe: "",
      dialogVisible: false,
      dialogAddVisible: false,
      annList: [],
      formAnn: {
        title: "",
        content: "",
      },
    };
  },
  methods: {
    handleTitle(data) {
      this.title = data.title;
      this.content = data.content;
      this.dialogVisible = true;
    },
    handleDelete(row) {
      this.$confirm("确认删除吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteAnnounce(row);

          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },
    deleteAnnounce(row) {
      var jsons = {
        ann_id: row.ann_id,
        token: sessionStorage.getItem("token"),
      };
      console.log("删除公告");
      console.log(jsons);
      this.axios
        .post("/api/course/delAnn/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.getAnnList();
          }
        });
    },

    handleAnn() {
      this.dialogAddVisible = true;
    },
    addAnn() {
      var jsons = {
        class_id: this.c_id,
        title: this.formAnn.title,
        content: this.formAnn.content,
        /*content: this.formAnn.content
          .replace(/\r\n/g, "<br/>")
          .replace(/\n/g, "<br/>")
          .replace(/\s/g, "&nbsp;"),*/
        token: sessionStorage.getItem("token"),
      };
      console.log("新增公告");
      console.log(jsons);
      this.axios
        .post("/api/course/addAnn/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.dialogAddVisible = false;
            this.formAnn.title = "";
            this.formAnn.content = "";
            this.getAnnList();
            this.$message("添加成功！");
          }
        });
    },

    getAnnList() {
      var jsons = {
        class_id: this.c_id,
        token: sessionStorage.getItem("token"),
      };

      console.log(jsons);
      this.axios
        .post("/api/course/getAnn/", JSON.stringify(jsons))
        .then((response) => {
          console.log("获得公告");
          console.log(response);

          this.annList = response.data.data;
        });
    },

    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.c_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      console.log("cid===" + this.c_id);
    },
  },
  mounted() {
    this.getParams();
    this.getAnnList();
  },
};
</script>

<style>
.el-button--danger {
  color: white;
}
.el-button--primary {
  color: white;
}
</style>

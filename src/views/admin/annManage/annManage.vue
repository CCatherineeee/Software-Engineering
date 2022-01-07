<template>
  <el-card color="#385F73" dark class="back">
    <p style="padding-top: 1%; font: 20px Microsoft YaHei; text-align: center">
      系统公告
    </p>
    <el-table
      :data="
        announceData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
      "
      style="width: 100%; margin-left: 2%; margin-right: 5%"
    >
      <el-table-column prop="date" label="发布时间"> </el-table-column>

      <el-table-column prop="title" label="主题">
        <template slot-scope="scope"
          ><el-link @click="handleTitle(scope.row)">{{
            scope.row.title
          }}</el-link>
        </template>
      </el-table-column>

      <el-table-column align="right"
        ><template #header>
          <v-btn color="primary" dark @click="handleAnn">
            新增公告
          </v-btn></template
        ><template slot-scope="scope">
          <v-row>
            <v-col cols="2">
              <v-btn color="primary" dark small @click="handleTitle(scope.row)"
                >查看</v-btn
              ></v-col
            >
            <v-col cols="2">
              <v-btn color="primary" dark small @click="handleDelete(scope.row)"
                >删除</v-btn
              ></v-col
            ></v-row
          >
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      layout="total, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pagesize"
      :total="announceData.length"
    >
    </el-pagination>

    <el-dialog :visible.sync="annCheckDialog" :title="this.title" center>
      <div v-html="formatImag(content)"></div>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="annCheckDialog = false"
          >确定</el-button
        >
      </div>
    </el-dialog>
    <el-dialog :visible.sync="annAddDialog" title="新增公告" center>
      <v-form lazy-validation>
        <el-input
          v-model="form.title"
          :counter="20"
          label="标题"
          filled
          required
        ></el-input>

        <br />
        <br />
        <br />

        <quill-editor
          v-model="form.content"
          label="内容"
          solo
          :counter="200"
        ></quill-editor>
      </v-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="addAnn">确定</el-button>
        <el-button type="primary" @click="annAddDialog = false">取消</el-button>
      </div>
    </el-dialog>
  </el-card>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      annCheckDialog: false,
      annAddDialog: false,

      currentPage: 1,
      pagesize: 10,
      title: "",
      content: "",
      announceData: [],
      form: {
        title: "输入标题",
        content: "请输入内容",
      },
    };
  },

  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleTitle(row) {
      this.title = row.title;
      this.content = row.content;
      this.annCheckDialog = true;
    },
    handleAnn() {
      this.annAddDialog = true;
    },
    handleDelete(row) {
      this.$confirm("确认删除公告吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteAnn(row);
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
    addAnn() {
      if (this.form.title == "") {
        this.$message({
          type: "warning",
          message: "公告标题不能为空!",
        });
      } else {
        var jsons = {
          content: this.form.content,
          title: this.form.title,
          token: sessionStorage.getItem("token"),
        };
        axios
          .post("/api//sys/addAnn/", JSON.stringify(jsons))
          .then((response) => {
            console.log("addAnn");
            console.log(response);
            this.annAddDialog = false;
            this.getAnn();
          })
          .catch((error) => {
            this.$message("网络错误！");
            console.log(error);
          });
      }
    },
    handleCheck() {},
    checkAnnounce() {},
    getAnn() {
      axios
        .get("/api/sys/getAnn/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getAnn");
          console.log(response);
          this.announceData = response.data;
        })
        .catch((error) => {
          this.$message("网络错误！");
          console.log(error);
        });
    },
    deleteAnn(row) {
      console.log("删除公告");
      console.log(row);
      var jsons = {
        annoucement_id: row.annoucement_id,
        token: sessionStorage.getItem("token"),
      };
      axios
        .post("/api/sys/delAnn/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          this.getAnn();
        })
        .catch((error) => {
          this.$message("网络错误！");
          console.log(error);
        });
    },
    formatImag(content) {
      return content.replace(
        /<img/g,
        "<img style='max-width:50%;height:auto;'"
      );
    },
  },
  mounted() {
    this.getAnn();
  },
};
</script>

<style scoped>
.dialogBack {
  margin: auto;
  font: 18px Microsoft YaHei;
}
.back {
  margin-left: 10%;
  margin-right: 10%;
  border-radius: 20px;
}
</style>

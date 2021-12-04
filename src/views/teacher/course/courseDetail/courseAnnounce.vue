<template>
  <div>
    <el-container>
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
            v-for="(data, index) in dataTable"
            :key="index"
            center
            placement="top"
            :timestamp="data.time"
          >
            <el-card>
              <h2>{{ data.title }}</h2>
              <p v-html="data.content"></p>

              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                size="mini"
                style="float: right; margin-left: 5px"
                @click="handleDelete(data.ann_id)"
              ></el-button>

              <el-button
                type="primary"
                icon="el-icon-edit"
                circle
                size="mini"
                style="float: right"
                @click="handleTitle(data)"
              ></el-button>
            </el-card>
          </el-timeline-item>
        </el-timeline>

        <el-dialog :visible.sync="dialogVisible" :title="this.title" center>
          <span class="dialogBack"
            ><el-input
              type="textarea"
              :rows="2"
              placeholder="请输入内容"
              v-model="content"
            >
            </el-input
          ></span>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="modifyAnn(content)"
              >确定</el-button
            >
            <el-button @click="dialogVisible = false">取消</el-button>
          </div>
        </el-dialog>
        <el-dialog :visible.sync="dialogAddVisible">
          <el-form
            :model="formAnn"
            ref="formAnn"
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
          <div slot="footer" class="dialog-footer">
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
import axios from "axios";

export default {
  data() {
    return {
      title: "",
      content: "",
      dialogVisible: false,
      dialogAddVisible: false,
      class_id : "",
      dataTable: [],
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
      axios.post("/api/course/delAnn/",JSON.stringify({
        ann_id : row
      }))
      this.getAnn()
    },
    modifyAnn(content) {
      this.dataTable.content = content;
      this.dialogVisible = false;
      document.execCommand("Refresh");
    },
    handleAnn() {
      this.dialogAddVisible = true;
    },
    addAnn() {
      this.dialogAddVisible = false;
      console.log(this.formAnn.content)
      this.axios.post("/api/course/addAnn/",JSON.stringify({
        class_id : this.class_id,
        title : this.formAnn.title,
        content : this.formAnn.content.replace(/\r\n/g, '<br/>').replace(/\n/g, '<br/>').replace(/\s/g, '&nbsp;')
      }))
      this.getAnn()
      this.formAnn.title = ""
      this.formAnn.content = ""
      this.$message("添加成功！")

    },
    getAnn(){
      this.axios.post(
          "/api/course/getAnn/",JSON.stringify(
              {
                class_id : this.class_id,
              }),
      ).then((response) => {
        //这里使用了ES6的语法
        console.log(response.data)
        this.dataTable = response.data
        //this.checkResponse(response.data); //请求成功返回的数据
      })
    }
  },
  mounted() {
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id']
    this.getAnn()
  }
};
</script>
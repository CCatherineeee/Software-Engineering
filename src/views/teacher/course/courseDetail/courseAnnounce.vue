<template>
  <div class="block">
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
              <el-link @click="handleTitle(data)">{{ data.content }}</el-link>

              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                size="mini"
                style="float: right; margin-left: 5px"
                @click="handleDelete(data.id)"
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
export default {
  data() {
    return {
      title: "",
      content: "",
      dialogVisible: false,
      dialogAddVisible: false,
      dataTable: [
        {
          time: "时间1",
          title: "标题1",
          content: "内容1",
          name: "人1",
        },
        {
          time: "2",
          title: "2.1",
          content: "2.2",
          name: "2.3",
        },
        {
          time: "3",
          title: "3.1",
          content: "3.2",
          name: "3.3",
        },
      ],
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
    deleteAnnounce() {},
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
    },
  },
};
</script>

<template>
  <div>
    <el-card>
      <el-table
        ref="filterTable"
        row-key="deadline"
        :data="
          tableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
        <el-table-column prop="experiment_title" label="实验名称">
          <template slot-scope="scope"
            ><el-link @click="toExperiment(scope.row)">{{
              scope.row.experiment_title
            }}</el-link>
          </template></el-table-column
        >
        <el-table-column prop="end_time" label="截止日期" sortable />
        <el-table-column prop="status" label="实验状态" sortable />
        <el-table-column prop="score" label="成绩" sortable />
        <el-table-column prop="is_submit" label="提交状态" sortable>
          <template slot-scope="scope">
            <el-tag
              v-if="scope.row.is_submit === true"
              key="已提交"
              type="success"
              effect="plain"
            >
              已提交
            </el-tag>

            <el-tag
              v-if="scope.row.is_submit === false"
              key="未提交"
              type="danger"
              effect="plain"
            >
              未提交
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="120%">
          <template slot-scope="scope">
            <el-button size="small" @click="toExperiment(scope.row)"
              >查看</el-button
            >

            <el-button
              size="small"
              @click="toExFill(scope.row)"
              v-if="
                scope.row.type === '在线提交' && scope.row.status === '未过期'
              "
              >在线填写</el-button
            >
            <el-button
              size="small"
              @click="handleUpload(scope.row)"
              v-if="
                scope.row.type === '提交文件' && scope.row.status === '未过期'
              "
              >上传文件</el-button
            >
            <el-button
              type="primary"
              plain
              size="small"
              @click="goToOnline(scope.row.ex_id, scope.row.end_time)"
              v-if="scope.row.online === 1 && scope.row.status === '未过期'"
              >在线模拟</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pagesize"
        layout="total,  prev, pager, next, jumper"
        :total="tableData.length"
        filterState
      >
      </el-pagination>
    </el-card>
    <el-dialog :visible.sync="fileDialog" title="上传实验报告" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileList"
        :multiple="true"
        :auto-upload="false"
        accept=""
      >
        <el-button type="primary">选取文件</el-button>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="fileDialog = false">取消</el-button>
        <el-button type="success" @click="uploadFile()">上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script >
export default {
  data() {
    return {
      sid: "",
      class_id: "",
      ex_id: "",
      currentPage: 1,
      pagesize: 7,
      tableData: [],
      fileList: [],
      fileDialog: false,
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    goToOnline(ex_id, end_time) {
      this.$router.push({
        path: "/studentHome/concreteCourse/onlineExp",
        query: {
          sid: this.sid,
          ex_id: ex_id,
          stop_time: end_time,
        },
      });
    },
    handlePreview(file) {
      console.log(file);
    },

    handleRemove(file) {
      this.fileList.pop(file);
    },

    handleChange(file) {
      this.fileList.push(file);
    },

    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    handleUpload(row) {
      this.fileDialog = true;
      this.ex_id = row.ex_id;
    },
    handleExamine() {
      this.$router.push({
        path: "/studentHome/concreteCourse/FillExper",
        query: { sid: this.sid },
      });
    },

    toExperiment(row) {
      this.$router.push({
        path: "/studentHome/concreteCourse/ConExper",
        query: {
          info: this.$Base64.encode(JSON.stringify(row.ex_id)),
        },
      });
    },
    toExFill(row) {
      this.$router.push({
        path: "/studentHome/concreteCourse/FillExper",
        query: {
          info: this.$Base64.encode(row.ex_id),
          title: this.$Base64.encode(row.experiment_title),
        },
      });
    },
    uploadFile() {
      console.log("uploadFile", this.fileList);
      let param = new FormData();
      this.fileList.forEach((file) => {
        param.append("report", file.raw);
      });
      param.append("s_id", this.sid);
      param.append("ex_id", this.ex_id);
      param.append("token", sessionStorage.getItem("token"));

      this.axios
        .post("/api/Ex/stuUpload/", param, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
        })
        .then((res) => {
          console.log("uploadFile", res);
          if (res.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (res.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            if (res.data["code"] === 200) {
              this.$message("上传成功");
              this.fileList = [];
              this.fileDialog = false;
              this.getEx();
            } else {
              this.$message("上传失败");
            }
          }
        });
    },
    getEx() {
      //"/api/class/showEx/"
      this.axios
        .post(
          "/api/class/showEx/",
          JSON.stringify({
            class_id: this.class_id,
            s_id: sessionStorage.getItem("id"),
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          //这里使用了ES6的语法
          //this.tableData = response.data
          //console.log("getEx");
          this.checkResponse(response.data); //请求成功返回的数据
        });
    },
    checkResponse(response) {
      console.log("getEx", response);
      if (response["code"] === 301) {
        this.$message("验证过期");
        this.$router.push({ path: "/login" });
      } else if (response["code"] === 404) {
        this.$message("找不到页面");
        this.$router.push({ path: "/404" });
      } else {
        this.tableData = [];
        for (var i = 0; i < response.data.length; i++) {
          if (response.data[i].status === 1) {
            response.data[i].status = "未过期";
            this.tableData.push(response.data[i]);
          } else if (response.data[i].status === 3) {
            response.data[i].status = "已过期";
            this.tableData.push(response.data[i]);
          }
          //this.tableData.push(response.data[i]);

          //this.tableData = response.data;
          //console.log();
          //console.log("thisTable", this.tableData);
        }
      }
    },
    getParams: function () {
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      this.sid = sessionStorage.getItem("id");
    },
  },
  mounted() {
    this.getParams();
    this.getEx();
  },
};
</script>

<style >
.el-button--primary {
  color: white;
}
.el-button--success {
  color: white;
}
</style>

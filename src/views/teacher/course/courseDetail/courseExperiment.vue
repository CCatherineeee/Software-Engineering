
<template>
  <div>
    <el-card>
      <el-row>
        <el-col :span="3">
          <v-btn
            color="orange lighten-2"
            dark
            @click="handleFile"
            style="margin-bottom: 10px"
          >
            pdf导入实验模板
          </v-btn></el-col
        >
      </el-row>
      <el-table
        ref="filterTable"
        row-key="deadline"
        :data="
          tableData.filter(
            (data) =>
              !search || data.name.toLowerCase().includes(search.toLowerCase())
          )
        "
        style="width: 100%"
      >
        <el-table-column prop="title" label="实验名称" sortable />
        <el-table-column prop="end_time" label="发布日期" sortable />
        <el-table-column prop="weight" label="权重" sortable />

        <el-table-column>
          <template #header>
            <el-input v-model="search" placeholder="请输入实验名称" />
          </template>
          <template #default="scope">
            <v-row>
              <v-col cols="6">
                <v-btn small dark @click="handleEdit(scope.row)"
                  >编辑实验模板</v-btn
                >
              </v-col>
              <v-col cols="3">
                <v-btn small dark @click="handleGrade(scope.row)"
                  >批改实验报告</v-btn
                >
              </v-col>
            </v-row>
          </template>
        </el-table-column>
      </el-table>

      <el-dialog
        :visible.sync="dialogVisible"
        title="请选择文件"
        center
        border-radius="4px"
      >
        <el-upload
          ref="uploadImport"
          action=""
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-change="handleChange"
          :before-remove="beforeRemove"
          :file-list="fileList"
          :multiple="true"
          :auto-upload="false"
          accept=""
        >
          <el-button type="primary" style="float: center">选取文件</el-button>
          <div slot="tip" class="el-upload__tip"></div>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="success">上传</el-button>
        </div>
      </el-dialog>
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
  </div>
</template>

<script >
export default {
  data() {
    return {
      dialogVisible: false,
      search: "",
      currentPage: 1,
      pagesize: 6,
      fileList: [],
      tableData: [],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handlePreview(file) {
      console.log(file);
    },

    handleRemove(file, fileListS) {
      console.log(file, fileListS);
    },

    handleChange(file) {
      console.log(file);
      this.fileListS.push(file);
      console.log(this.fileListS);
    },

    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    handleEdit(row) {
      console.log(row);
      this.$router.push({
        path: "/teacherHome/concreteCourse/addExper",
        query: { id: row.id },
      });
    },

    handleGrade(row) {
      console.log(row);
      this.$router.push({
        path: "/teacherHome/concreteCourse/stuExperList",
        query:{
          info : this.$Base64.encode(JSON.stringify({"ex_id" : row.ex_id}))}
      });
    },

    handleFile() {
      this.dialogVisible = true;
    },
    checkResponse(response){
      this.tableData = response
      }
  },
  mounted() {
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id']
    this.axios.post(
        "/api/course/getEx/",JSON.stringify(
            {
              c_id : this.class_id.substring(0,12)
            }),
    ).then((response) => {
      //这里使用了ES6的语法
      //this.tableData = response.data
      this.checkResponse(response.data); //请求成功返回的数据
    })
  },
};
</script>
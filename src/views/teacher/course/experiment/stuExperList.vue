
<template>
  <div>
    <el-card>
      <v-btn
        color="orange lighten-2"
        dark
        @click="releaseGrade"
        style="margin-bottom: 10px; margin-right: 10px"
      >
        发布成绩
      </v-btn>
      <v-btn
        color="orange lighten-2"
        dark
        @click="downloadSelect"
        style="margin-bottom: 10px"
      >
        批量下载
      </v-btn>
      <el-table
        ref="filterTable"
        row-key="score"
        @selection-change="handleSelectionChange"
        :data="
          tableData.filter(
            (data) =>
              !search ||
              data.sid.toLowerCase().includes(search.toLowerCase()) ||
              data.name.toLowerCase().includes(search.toLowerCase())
          )
        "
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="s_id" label="学号" sortable />
        <el-table-column prop="s_name" label="姓名" sortable />
        <el-table-column prop="status" label="是否提交" sortable />
        <el-table-column prop="submitTime" label="提交日期" sortable />
        <el-table-column prop="score" label="分数" sortable />
        <el-table-column prop="grader" label="批改人"  />

        <el-table-column>
          <template #header>
            <el-input v-model="search" placeholder="请输入" />
          </template>
          <template #default="scope">
            <v-row>
              <v-col cols="3">
                <v-btn small dark @click="handleGrade(scope.row)">打分</v-btn>
              </v-col>
              <v-col cols="3">
                <v-btn small dark @click="download(scope.row)">下载</v-btn>
              </v-col>
            </v-row>
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
  </div>
</template>

<script >
export default {
  data() {
    return {
      search: "",
      currentPage: 1,
      ex_id:"",
      pagesize: 6,
      multipleSelection: [],

      tableData: [
        { sid: "1", name: "1", submit: "2021.11.1", score: "2022.2.2" },
      ],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    handleGrade(row) {
      this.$router.push({
        path: "/teacherHome/concreteCourse/stuExper",
        query: { sid: row.sid },
      });
    },

    releaseGrade() {
      //发布成绩
    },
    downloadSelect() {
      //批量下载学生的pdf
    },
    download(row){
      console.log(row.s_id)
      let formData = new FormData()
      formData.append('s_id',row.s_id);
      formData.append('ex_id',this.ex_id);
      this.axios.post("/api/tea/Ex/getReport/",formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            },
        responseType: "blob"

          }
      ).then((response)=>{

        const fileName = response.headers['content-disposition'];
        var fname = fileName.split("filename*=UTF-8''")[1]
        fname = decodeURIComponent(fname)
        //const title = fileName && (fileName.indexOf('filename=') !== -1) ? fileName.split('=')[1] : 'download';

        const blob = new Blob([response.data],{type:'text/plain,charset=UTF-8'});
        var downloadElement = document.createElement("a");
        var href = window.URL.createObjectURL(blob);
        downloadElement.href = href;

        downloadElement.download = fname
        document.body.appendChild(downloadElement);
        downloadElement.click();
        document.body.removeChild(downloadElement);
        window.URL.revokeObjectURL(href);
         /*
        href.href = window.URL.createObjectURL(blob);
        href.target = "_blank";
        href.click();
          */
        //console.log(response)
      })
    }
  },
  mounted() {
    this.ex_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['ex_id']
    this.axios.post(
        "/api/tea/Ex/getReportList/",JSON.stringify(
            {
              ex_id : this.ex_id
            }),
    ).then((response) => {
      this.tableData = response.data
    })
  },
};
</script>

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
        <el-table-column prop="sid" label="学号" sortable />
        <el-table-column prop="name" label="姓名" sortable />
        <el-table-column prop="submit" label="提交日期" sortable />
        <el-table-column prop="score" label="分数" sortable />

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
                <v-btn small dark>下载</v-btn>
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
  },
  mounted() {
    //获取所有实验信息
  },
};
</script>
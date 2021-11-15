
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
        <el-table-column prop="name" label="实验名称" sortable />
        <el-table-column prop="release" label="发布日期" sortable />
        <el-table-column prop="deadline" label="截止日期" sortable />

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" @click="handleCheck(scope.row)"
              >查看实验指导</el-button
            >
            <el-button size="small" @click="handleExamine()"
              >查看我的报告</el-button
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
  </div>
</template>

<script >
export default {
  data() {
    return {
      sid: "",
      currentPage: 1,
      pagesize: 6,
      tableData: [{ name: "1", release: "2021.11.1", deadline: "2022.2.2" }],
    };
  },
  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },

    handleCheck(row) {
      console.log(row);
      this.$router.push({
        path: "/home/concreteCourse/ConExper",
        query: { release: row.id },
      });
    },

    handleExamine() {
      this.$router.push({
        path: "/home/concreteCourse/FillExper",
        query: { sid: this.sid },
      });
    },
  },
  mounted() {
    //获取所有实验信息
  },
};
</script>
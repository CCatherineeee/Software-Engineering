
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
        <el-table-column prop="title" label="实验名称" sortable />
        <el-table-column prop="end_time" label="发布日期" sortable />
        <el-table-column prop="weight" label="权重" sortable />

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
      tableData: [],
      class_id : ""
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
        path: "/studentHome/concreteCourse/ConExper",
        query: { release: row.id },
      });
    },

    handleExamine() {
      this.$router.push({
        path: "/studentHome/concreteCourse/FillExper",
        query: { sid: this.sid },
      });
    },
    checkResponse(response){

      for(var i=0; i<response.length;i++){
        if (response[i]['status'] == 0){
          this.tableData.add(response[i])
        }
      }
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
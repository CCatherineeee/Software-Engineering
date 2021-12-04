<template>
  <div>
    <el-table
      ref="filterTable"
      row-key="id"
      :data="
        tableData.filter(
          (data) =>
            !search ||
            data.title.toLowerCase().includes(search.toLowerCase()) ||
            data.upload.toLowerCase().includes(search.toLowerCase()) ||
            data.modify.toLowerCase().includes(search.toLowerCase()) ||
            data.author.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
    >
      <el-table-column prop="title" label="文件名" sortable />

      <el-table-column>
        <template #header>
          <el-input v-model="search" />
        </template>
        <template #default="scope">
          <el-button size="mini" @click="handleCheck(scope.row)"
            >查看</el-button
          >
          <el-button size="mini" type="primary" @click="handleDown(scope.row)"
            >下载</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="tableData.length"
    >
    </el-pagination>

    <el-dialog :visible.sync="dialog" center>
      <el-descriptions
        direction="vertical"
        :column="1"
        border
        size="medium"
        title="实验指导"
      >
        <el-descriptions-item label="实验名称"
          >kooriookami</el-descriptions-item
        >
        <el-descriptions-item label="实验目的"
          >18100000000</el-descriptions-item
        >
        <el-descriptions-item label="实验设备" :span="2"
          >苏州市</el-descriptions-item
        >

        <el-descriptions-item label="实验步骤"
          >江苏省苏州市吴中区吴中大道 1188 号</el-descriptions-item
        >
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialog = false">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      currentPage: 1,
      pagesize: 6,
      dialog: false,
      class_id : "",
      tableData: [],
    };
  },
  methods: {
    toFile() {
      this.$router.push("/studentHome/concreteCourse/concreteFile");
    },
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleCheck() {
      this.dialog = true;
    },
    handleDown(row) {
      console.log(row);
    },
  },
  mounted() {
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id'];
    this.axios.post(
        "/api/manageClassFileRoute/getClassFile",JSON.stringify(
            {
              class_id : this.class_id
            }),
    ).then((response) => {
      //这里使用了ES6的语法
      //this.tableData = response.data
      this.tableData = response.data; //请求成功返回的数据
    })
  }
};
</script>

<style scoped>
.el-divider--vertical {
  display: inline-block;
  width: 1px;
  height: 100%;
  margin: 0 8px;
  vertical-align: middle;
  position: relative;
}
</style>

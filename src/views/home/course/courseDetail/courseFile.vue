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
      <el-table-column prop="upload" label="上传时间" sortable />
      <el-table-column prop="modify" label="修改时间" sortable />
      <el-table-column prop="author" label="修改者" sortable />

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
      items: [
        {
          id: 1,
          name: "我的文件",
        },
        {
          id: 5,
          name: "课程文件1",
          children: [
            {
              id: 6,
              name: "vuetify :",
              children: [
                {
                  id: 7,
                  name: "src :",
                  children: [
                    { id: 8, name: "index : ts" },
                    { id: 9, name: "bootstrap : ts" },
                  ],
                },
              ],
            },
            {
              id: 10,
              name: "material2 :",
              children: [
                {
                  id: 11,
                  name: "src :",
                  children: [
                    { id: 12, name: "v-btn : ts" },
                    { id: 13, name: "v-card : ts" },
                    { id: 14, name: "v-window : ts" },
                  ],
                },
              ],
            },
          ],
        },
        {
          id: 15,
          name: "课程文件2",
          children: [
            { id: 16, name: "October : pdf" },
            { id: 17, name: "November : pdf" },
            { id: 18, name: "Tutorial : html" },
          ],
        },
        {
          id: 19,
          name: "课程文件3",
          children: [
            {
              id: 20,
              name: "Tutorials :",
              children: [
                { id: 21, name: "Basic layouts : mp4" },
                { id: 22, name: "Advanced techniques : mp4" },
                { id: 23, name: "All about app : dir" },
              ],
            },
            { id: 24, name: "Intro : mov" },
            { id: 25, name: "Conference introduction : avi" },
          ],
        },
      ],

      tableData: [
        {
          title: "wenjian1",
          upload: "1",
          modify: "1",
          author: "1",
        },
      ],
    };
  },
  methods: {
    toFile() {
      this.$router.push("/home/concreteCourse/concreteFile");
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

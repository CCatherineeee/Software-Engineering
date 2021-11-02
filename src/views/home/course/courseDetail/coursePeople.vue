<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="所有人" name="first">
      <el-table :id="tableData" style="width: 100%">
        <el-table-column prop="id" label="学号"> </el-table-column>
        <el-table-column prop="name" label="姓名"> </el-table-column>
        <el-table-column prop="role" label="身份" style="float: right">
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="小组" name="second">配置管理</el-tab-pane>
  </el-tabs>
</template>

<script>
export default {
  id() {
    return {
      activeName: "second",
      tableData: [
        {
          name: "王小虎",
          id: "2016-05-02",
          role: "上海市普陀区金沙江路 1518 弄",
        },
        {
          id: "2016-05-04",
          name: "王小虎",
          role: "上海市普陀区金沙江路 1517 弄",
        },
        {
          id: "2016-05-01",
          name: "王小虎",
          role: "上海市普陀区金沙江路 1519 弄",
        },
        {
          id: "2016-05-03",
          name: "王小虎",
          role: "上海市普陀区金沙江路 1516 弄",
        },
      ],
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
};
</script>
<template>
  <div>
    <el-card>
      <el-button type="danger" @click="handleCheckCancel">批量注销</el-button>
      <el-button @click="toggleSelection()">取消选择</el-button>

      <el-table
        ref="filterTable"
        row-key="date"
        :data="
          tableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"> </el-table-column>
        <el-table-column prop="name" label="姓名" sortable />
        <el-table-column prop="id" label="学号" sortable />
        <el-table-column
          prop="identity"
          label="身份权限"
          sortable
          :filters="[
            { text: '学生', value: 'student' },
            { text: '助教', value: 'assistant' },
            { text: '教师', value: 'professor' },
            { text: '责任教师', value: 'mainProfessor' },
          ]"
          :filter-method="filterIdentity"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.identity === 'student'">学生</span>
            <span v-if="scope.row.identity === 'assistant'">助教</span>
            <span v-if="scope.row.identity === 'professor'">教师</span>
            <span v-if="scope.row.identity === 'mainProfessor'">责任教师</span>
          </template>
        </el-table-column>

        <el-table-column
          prop="state"
          label="状态"
          sortable
          :filters="[
            { text: '激活', value: 'activate' },
            { text: '非激活', value: 'nonactivate' },
          ]"
          :filter-method="filterState"
          filter-placement="bottom-end"
        >
          <template #default="scope">
            <el-tag
              :type="scope.row.state === 'activate' ? 'success' : 'danger'"
              disable-transitions
              ><span v-if="scope.row.state === 'activate'">激活</span>
              <span v-if="scope.row.state === 'nonactivate'"
                >非激活</span
              ></el-tag
            >
          </template>
        </el-table-column>

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small" @click="handleCheck(scope.row)"
              >查看</el-button
            >
            <el-button size="small" type="danger" @click="handleCheckCancel"
              >注销</el-button
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
    </el-card>
  </div>
</template>

<script >
export default {
  data() {
    return {
      currentPage: 1,
      pagesize: 6,
      tableData: [
        {
          name: "Tom",
          id: "1",
          identity: "student",
          state: "activate",
        },
        {
          name: "Tomy",
          id: "2",
          identity: "assistant",
          state: "activate",
        },
        {
          name: "Ann",
          id: "3",
          identity: "professor",
          state: "activate",
        },
        {
          name: "Jim",
          id: "4",
          identity: "mainProfessor",
          state: "activate",
        },
        {
          name: "kim",
          id: "5",
          identity: "mainProfessor",
          state: "nonactivate",
        },
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

    handleCheck(row) {
      console.log(row);
      this.$router.push("/adminHome/accountInfo");
    },

    filterState(value, row) {
      return row.state === value;
    },
    filterIdentity(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },

    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    toggleSelection() {
      this.$refs.filterTable.clearSelection();
    },

    cancelAccount() {
      //注销账户
    },

    handleCheckCancel() {
      this.$confirm("确认注销账户吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.cancelAccount();

          this.$message({
            type: "success",
            message: "注销成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消注销操作",
          });
        });
    },
  },
};
</script>
<template>
  <div>
    <el-card>
      <el-table
        ref="filterTable"
        row-key="date"
        :data="
          tableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
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
            <el-button size="small" type="danger" @click="handleEdit(scope.row)"
              >编辑</el-button
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
import axios from "axios";
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

    handleEdit(row) {
      console.log(row);
      this.$router.push("/adminHome/accountModify");
    },

    filterState(value, row) {
      return row.state === value;
    },
    filterIdentity(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
  },
  mounted() {
    //获取所有用户所有信息
    axios
      .get("/api/getUserInfo/allUser/", {
        //params: { userData: "value" },
        crossDomain: true,
      })
      .then((response) => (this.userData = response.data))
      .catch(function (error) {
        console(error);
      });
  },
};
</script>
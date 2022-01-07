<!-- 查看页面-->
<template>
  <div>
    <el-card>
      <el-table
        ref="filterTable"
        :data="
          tableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
        <el-table-column prop="name" label="姓名" sortable />
        <el-table-column prop="id" label="学号" sortable />
        <el-table-column
          prop="role"
          label="身份权限"
          sortable
          :filters="[
            { text: '学生', value: 1 },

            { text: '教师', value: 2 },
            { text: '助教', value: 3 },
          ]"
          :filter-method="filterIdentity"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.role === 1">学生</span>

            <span v-if="scope.row.role === 2">教师</span>
            <span v-if="scope.row.role === 3">助教</span>
          </template>
        </el-table-column>

        <el-table-column
          prop="is_active"
          label="状态"
          sortable
          :filters="[
            { text: '激活', value: 1 },
            { text: '非激活', value: 0 },
          ]"
          :filter-method="filterState"
          filter-placement="bottom-end"
        >
          <template #default="scope">
            <el-tag
              :type="scope.row.is_active === 1 ? 'success' : 'danger'"
              disable-transitions
              ><span v-if="scope.row.is_active === 1">激活</span>
              <span v-if="scope.row.is_active === 0">非激活</span></el-tag
            >
          </template>
        </el-table-column>

        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              class="button"
              size="small"
              @click="handleCheck(scope.row)"
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
        layout="total, prev, pager, next, jumper"
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

    handleCheck(row) {
      console.log(row);
      this.$router.push({
        path: "/adminHome/userManage/accountInfo",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ id: row.id, role: row.role })
          ),
        },
      });
    },

    handleEdit(row) {
      console.log(row);
      this.$router.push({
        path: "/adminHome/userManage/accountModify",
        query: {
          info: this.$Base64.encode(
            JSON.stringify({ id: row.id, role: row.role })
          ),
        },
      });
    },

    filterState(value, row) {
      return row.is_active === value;
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
        crossDomain: true,
      })
      .then((response) => (this.tableData = response.data))
      .catch(function () {});

    //console.log(this.userData);
  },
};
</script>

<style scoped>
.button {
  background: #7986cb;
  color: white;
}
.button:hover {
  color: yellow;
}
.el-button--danger {
  color: white;
}
</style>
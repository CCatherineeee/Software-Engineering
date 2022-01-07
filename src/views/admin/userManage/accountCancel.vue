<template>
  <div>
    <el-scrollbar>
      <el-card>
        <el-table
          ref="multipleTable"
          :data="
            userData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
          "
          style="width: 100%"
        >
          <el-table-column prop="name" label="姓名" sortable />
          <el-table-column prop="id" label="学号/工号" sortable />
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
              <el-button size="small" @click="handleCheck(scope.row)"
                >查看</el-button
              >
              <el-button
                size="small"
                type="danger"
                @click="handleCheckCancelO(scope.row)"
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
          layout="total,prev, pager, next, jumper"
          :total="userData.length"
        >
        </el-pagination>
      </el-card>
    </el-scrollbar>
  </div>
</template>

<script >
import axios from "axios";
export default {
  data() {
    return {
      currentPage: 1,
      pagesize: 6,
      multipleSelection: [],
      userData: [],
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
      this.$refs.multipleTable.clearSelection();
    },

    cancelOneAccount(row) {
      //注销单个账户
      console.log("id==" + row.id);
      console.log("token==" + sessionStorage.getItem("token"));
      if (row.role == 1) {
        axios
          .post(
            "/api/delete/student/",
            JSON.stringify({
              s_id: row.id,
              token: sessionStorage.getItem("token"),
            })
          )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
      } else if (row.role == 2) {
        axios
          .post(
            "/api/delete/teacher/",
            JSON.stringify({
              t_id: row.id,
              token: sessionStorage.getItem("token"),
            })
          )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
      } else if (row.role == 3) {
        axios
          .post(
            "/api/delete/Ta/",
            JSON.stringify({
              ta_id: row.id,
              token: sessionStorage.getItem("token"),
            })
          )
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
      }
      this.getUserData();
    },

    handleCheckCancelO(row) {
      this.$confirm("确认注销账户吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.cancelOneAccount(row);

          this.$message({
            type: "success",
            message: "注销成功!",
          });
          this.getUserData();
          //document.execCommand("Refresh");
          //location.reload();
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消注销操作",
          });
        });
      this.getUserData();
    },

    getUserData() {
      //获取所有用户所有信息
      axios
        .get("/api/getUserInfo/allUser/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => (this.userData = response.data))
        .catch(function () {});
    },
  },
  mounted() {
    this.getUserData();

    //console.log(this.userData);
  },
};
</script>

<style scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
  overflow-y: hidden;
}
.el-button--danger {
  color: white;
}
.el-button--primary {
  color: white;
}
</style>
<!--  教师查看自己名下所有责任课程 -->-->
<template>
  <div>
    <el-table
      class="tableBack"
      ref="filterTable"
      :data="
        tableData
          .filter(
            (data) =>
              !search ||
              data.course_id.toLowerCase().includes(search.toLowerCase()) ||
              data.name.toLowerCase().includes(search.toLowerCase()) ||
              data.year.toLowerCase().includes(search.toLowerCase()) ||
              data.semester.toLowerCase().includes(search.toLowerCase())
          )
          .slice((currentPage - 1) * pagesize, currentPage * pagesize)
      "
    >
      <el-table-column prop="course_id" label="课程编号" sortable />
      <el-table-column prop="name" label="课程名称" sortable />
      <el-table-column prop="year" label="课程学年" sortable />
      <el-table-column prop="semester" label="课程学期" sortable>
      </el-table-column>

      <el-table-column>
        <template #header>
          <el-input v-model="search" placeholder="Type to search" />
        </template>
        <template slot-scope="scope">
          <el-button size="small" @click="handleExam(scope.row)"
            >管理班级</el-button
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
  </div>
</template>

<script >
export default {
  data() {
    return {
      dialogVisible: false,
      search: "",
      currentPage: 1,
      pagesize: 10,
      tableData: [],

      form: {
        title: "",
        reason: "",
        hour: "",
        credit: "",
      },

      courseExist: [],
      timeout: null,
    };
  },
  methods: {
    getParams: function () {
      this.id = sessionStorage.getItem("id");
    },
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },

    handleManage(row) {
      console.log(row);
      this.$router.push({
        path: "/teacherHome/courseClass",
        query: {
          c_id: row.course_id,
          name: row.name,
          prefix: row.prefix,
          semester: row.semester,
          year: row.year,
        },
      });
    },
    handleExam(row) {
      console.log(row);
      this.$router.push({
        path: "/teacherHome/duty-course/courseInfo",

        query: {
          info: this.$Base64.encode(
            JSON.stringify({
              course_id: row.course_id,
              name: row.name,
              prefix: row.prefix,
              semester: row.semester,
              year: row.year,
            })
          ),
        },
      });
    },

    getCourse() {
      this.axios
        .post(
          "/api/course/myDuty/",
          JSON.stringify({
            t_id: this.id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else {
            this.tableData = response.data["data"]; //请求成功返回的数据
          }
        });
    },
  },

  mounted() {
    this.getParams();
    this.getCourse();
  },
};
</script>

<style scoped>
.tableBack {
  width: 100%;
  margin-top: 10px;
}
.el-button--primary {
  color: white;
}
</style>

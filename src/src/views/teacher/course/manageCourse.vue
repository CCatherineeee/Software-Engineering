<!-- 查看页面-->
<template>
  <div>
    <v-btn color="orange lighten-2" dark @click="handleDialog">
      开课申请
    </v-btn>
    <el-table
      class="tableBack"
      ref="filterTable"
      :data="
        tableData.filter(
          (data) =>
            !search ||
            data.title.toLowerCase().includes(search.toLowerCase()) ||
            data.id.toLowerCase().includes(search.toLowerCase()) ||
            data.date.toLowerCase().includes(search.toLowerCase()) ||
            data.place.toLowerCase().includes(search.toLowerCase())
        )
      "
    >
      <el-table-column prop="id" label="课程编号" sortable />
      <el-table-column prop="title" label="课程名称" sortable />
      <el-table-column prop="date" label="上课时间" sortable />
      <el-table-column prop="place" label="上课地点" sortable />

      <el-table-column>
        <template #header>
          <el-input v-model="search" placeholder="Type to search" />
        </template>
        <template slot-scope="scope">
          <el-button size="small" @click="handleManage(scope.row)"
            >课程管理</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogVisible" title="请输入课程信息" center>
      <el-form :model="form" ref="form" style="margin: 10px 105px 0px 85px">
        <el-form-item
          label="名称"
          :required="true"
          prop="title"
          status-icon="true"
        >
          <el-autocomplete
            v-model="form.title"
            :fetch-suggestions="querySearchAsync"
            value-key="title"
            autocomplete="off"
          ></el-autocomplete>
        </el-form-item>

        <el-form-item
          label="预计学时"
          prop="hour"
          status-icon="true"
          :required="true"
        >
          <el-input v-model="form.hour"></el-input>
        </el-form-item>

        <el-form-item
          label="申请学分"
          prop="credit"
          status-icon="true"
          :required="true"
        >
          <el-input v-model="form.credit"></el-input>

          <el-form-item
            label="开课理由"
            :required="true"
            prop="reason"
            status-icon="true"
          >
            <el-input
              v-model="form.reason"
              type="textarea"
              placeholder="200字以内"
              maxlength="200"
              show-word-limit
            ></el-input>
          </el-form-item>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="add()">确定</el-button>
      </div>
    </el-dialog>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
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
      pagesize: 6,
      tableData: [
        {
          title: "王小虎",
          id: "2016-05-02",
          date: " 1",
          place: "1",
        },
        {
          id: "2016-05-04",
          title: "王小虎",
          date: " 1",
          place: "1",
        },
        {
          id: "2016-05-01",
          title: "王小虎",
          date: " 1",
          place: "1",
        },
        {
          id: "2016-05-03",
          title: "王小虎",
          date: " 1",
          place: "1",
        },
      ],

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
        query: { id: row.id },
      });
    },

    handleDialog() {
      this.dialogVisible = true;
    },
    add() {
      console.log(this.form);
      if (this.isExist) {
        this.$message("该课程已存在！");
        this.dialogVisible = true;
      } else this.dialogVisible = false;
    },
    isExist() {
      var ret = this.courseExist.indexOf(this.form.title);
      return ret > 0;
    },

    querySearchAsync(queryString, cb) {
      var courseExist = this.courseExist;
      var results = queryString
        ? courseExist.filter(this.createStateFilter(queryString))
        : courseExist;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 3000 * Math.random());
    },

    createStateFilter(queryString) {
      return (data) => {
        return (
          data.title.toLowerCase().indexOf(queryString.toLowerCase()) === 0
        );
      };
    },

    loadAll() {
      return [
        { title: "三全鲜食（北新泾店）" },
        {
          title: "Hot honey 首尔炸鸡（仙霞路）",
        },
      ];
    },
  },

  mounted() {
    this.courseExist = this.loadAll();
  },
};
</script>

<style scoped>
.tableBack {
  width: 100%;
  margin-top: 10px;
}
</style>
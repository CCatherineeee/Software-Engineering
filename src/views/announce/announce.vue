<template>
  <el-container style="margin-top: 20px">
    <el-main class="background">
      <p
        style="
          padding-top: 20px;
          font: 20px Microsoft YaHei;
          text-align: center;
        "
      >
        系统公告
      </p>
      <el-table
        :data="
          announceData.slice(
            (currentPage - 1) * pagesize,
            currentPage * pagesize
          )
        "
        style="width: 100%"
      >
        <el-table-column prop="date" label="发布时间" width="200px">
        </el-table-column>

        <el-table-column prop="title" label="主题" width="450px">
          <template slot-scope="scope"
            ><el-link @click="handleTitle(scope.row)">{{
              scope.row.title
            }}</el-link>
          </template>
        </el-table-column>

        <el-table-column label="操作"
          ><template slot-scope="scope">
            <el-button
              size="small"
              type="primary"
              @click="handleTitle(scope.row)"
              >查看</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        layout="total, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pagesize"
        :total="announceData.length"
      >
      </el-pagination>

      <el-dialog :visible.sync="dialogVisible" :title="this.title" center>
        <div v-html="formatImag(content)"></div>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="dialogVisible = false"
            >确定</el-button
          >
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      dialogVisible: false,
      currentPage: 1,
      pagesize: 6,
      title: "",
      content: "",
      announceData: [],
    };
  },

  methods: {
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleTitle(row) {
      this.title = row.title;
      this.content = row.content;
      this.dialogVisible = true;
    },
    handleCheck() {},
    checkAnnounce() {},
    formatImag(content) {
      return content.replace(
        /<img/g,
        "<img style='max-width:60%;height:auto;'"
      );
    },
  },
  mounted() {
    axios
      .get("/api/sys/getAnn/", {
        params: { token: sessionStorage.getItem("token") },
        crossDomain: true,
      })
      .then((response) => {
        console.log(response);

        this.announceData = response.data;
      })
      .catch(function (error) {
        console.log(error);
      });
  },
};
</script>

<style scoped>
.table {
  margin: auto;
}
.background {
  background-color: white;
  border-radius: 15px;
  margin-left: 15%;
  margin-right: 15%;
}
.dialogBack {
  margin: auto;
  font: 18px Microsoft YaHei;
}
.el-button--primary {
  color: white;
}
</style>

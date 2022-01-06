<template>
  <div>
    <h1 style="color: #409eff">消息页面</h1>
    <el-divider></el-divider>
    <h3>欢迎！</h3>
    <!-- <el-container style="margin-top:20px;">
      <el-main >
        <el-calendar v-model="value"></el-calendar>
      </el-main>
    </el-container> -->
    <el-card class="box-card" style="margin-top: 20px; height: 460px">
      <el-collapse
        v-model="activeName"
        v-for="item in msgList.slice(
          (currentPage - 1) * pagesize,
          currentPage * pagesize
        )"
        :key="item.stu_message_id"
        accordion
      >
        <el-collapse-item
          :title="item.create_time + item.title"
          :name="item.seq"
          style="color: #666666"
          v-if="item.is_read == 1"
        >
          <div>
            {{ item.content }}
            <el-button
              type="danger"
              icon="el-icon-delete"
              style="float: right"
              @click="deleteMsg(item.stu_message_id)"
              circle
            ></el-button>
          </div>
        </el-collapse-item>
        <el-collapse-item
          :title="item.create_time + item.title"
          :name="item.seq"
          style="color: #cc0033"
          v-if="item.is_read == 0"
          @click.native="isRead(item.stu_message_id)"
        >
          <div>{{ item.content }}</div>
        </el-collapse-item>
      </el-collapse>

      <el-pagination
        layout="total, prev, pager, next, jumper"
        :total="lenList"
        class="pig"
        @current-change="handleCurrentChange"
        float="buttom"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value: new Date(),
      activeName: "0",
      msgList: [],
      lenList: 0,
      pagesize: 8,
      currentPage: 1,
      s_id: sessionStorage.getItem("id"),
    };
  },
  mounted() {
    this.getStudentMsg();
  },
  methods: {
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    getStudentMsg() {
      var json = {
        s_id: this.s_id,
      };
      var that = this;
      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/getStuMessage",
          JSON.stringify(json)
        )
        .then(
          function (response) {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) that.$message("找不到学生");
            else {
              console.log("getStudentMsg", response);
              var stuMsgList = response.data;
              console.log(stuMsgList);
              for (var i = 0; i < stuMsgList.not_read.length; i++) {
                that.msgList.push(stuMsgList.not_read[i]);
                that.lenList += 1;
              }
              for (i = 0; i < stuMsgList.read.length; i++) {
                that.msgList.push(stuMsgList.read[i]);
                that.lenList += 1;
              }
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
    isRead(stu_message_id) {
      var json = {
        s_id: this.s_id,
        stu_message_id: stu_message_id,
      };
      console.log(json);
      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/changeStuMessage",
          JSON.stringify(json)
        )
        .then(
          function (response) {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) this.$message("找不到学生");
            else if (response.data.status === 500) {
              this.$message("该条消息不存在或被删除");
            } else {
              this.getStudentMsg();
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
    deleteMsg(stu_message_id) {
      var json = {
        s_id: this.s_id,
        stu_message_id: stu_message_id,
      };
      var that = this;
      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/deleteStuMessage",
          JSON.stringify(json)
        )
        .then(
          function (response) {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) this.$message("找不到学生");
            else if (response.data.status === 500) {
              this.$message("该条消息不存在或被删除");
            } else {
              console.log(response.data);
              that.$message("删除成功");
              this.getStudentMsg();
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
  },
};
</script>

<style >
.el-button--danger {
  color: white;
}
</style>
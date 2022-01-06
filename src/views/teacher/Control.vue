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
        :key="item.tea_message_id"
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
              @click="handleDelete(item.tea_message_id)"
              circle
            ></el-button>
          </div>
        </el-collapse-item>
        <el-collapse-item
          :title="item.create_time + item.title"
          :name="item.seq"
          style="color: #cc0033"
          v-if="item.is_read == 0"
          @click.native="isRead(item.tea_message_id)"
        >
          <div>{{ item.content }}</div>
        </el-collapse-item>
      </el-collapse>
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

      pagesize: 8,
      currentPage: 1,
      t_id: sessionStorage.getItem("id"),
    };
  },

  methods: {
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    handleDelete(row) {
      this.$confirm("确认删除吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteMsg(row);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除",
          });
        });
    },
    getTeadentMsg() {
      var json = {
        t_id: this.t_id,
      };

      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/getTeacherMessage",
          JSON.stringify(json)
        )
        .then(
          (response) => {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) this.$message("找不到老师");
            else {
              var MsgList = response.data;
              console.log("MsgList", MsgList);
              this.msgList = MsgList.not_read;
              for (var i = 0; i < MsgList.read.length; i++) {
                this.msgList.push(MsgList.read[i]);
              }
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
    isRead(tea_message_id) {
      var json = {
        t_id: this.t_id,
        tea_message_id: tea_message_id,
      };

      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/changeTeacherMessage",
          JSON.stringify(json)
        )
        .then(
          (response) => {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) this.$message("找不到教师");
            else if (response.data.status === 500) {
              this.$message("该条消息不存在或被删除");
            } else {
              this.getTeadentMsg();
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
    deleteMsg(tea_message_id) {
      var json = {
        t_id: this.t_id,
        tea_message_id: tea_message_id,
      };
      var that = this;
      this.axios
        .post(
          //"/api/users/validateCaptcha"
          "/api/message/deleteTeacherMessage",
          JSON.stringify(json)
        )
        .then(
          (response) => {
            //这里使用了ES6的语法
            // this.checkResponse(response.data); //请求成功返回的数据
            if (response.data.status === 400) this.$message("找不到老师");
            else if (response.data.status === 500) {
              this.$message("该条消息不存在或被删除");
            } else {
              that.getTeadentMsg();
            }
          },
          function (err) {
            console.log(err);
          }
        );
    },
  },
  mounted() {
    this.getTeadentMsg();
  },
};
</script>

<style>
.el-button--danger {
  color: white;
}
</style>
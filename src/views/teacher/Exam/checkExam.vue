<template>
  <el-table
      :data="examList">
    <el-table-column
        prop="title"
        label="名称"
        width="170">
    </el-table-column>
    <el-table-column
        prop="start_time"
        label="起始时间"
        width="180">
    </el-table-column>
    <el-table-column
        prop="end_time"
        label="截止时间"
        width="180">
    </el-table-column>
    <el-table-column
        width="80"
        prop="status"
        label="状态">
      <template #default="scope">
        <el-tag
            :key="scope.row.status"
            :type="scope.row.type"
            effect="plain">
          {{ scope.row.status }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <div v-if="scope.row.status==='未开放'">
          <el-button type="primary" @click="editExamTime(scope.row)">修改</el-button>
          <el-button type="primary" @click="pushExam(scope.row)">开放</el-button>
          <el-button type="primary" @click="lookExam(scope.row)">查看</el-button>
        </div>
        <div v-if="scope.row.status==='进行中'">
          <el-button type="primary" @click="stopExam(scope.row)">中止</el-button>
          <el-button type="primary" @click="lookExam(scope.row)">查看</el-button>

        </div>
        <div v-if="scope.row.status==='已截止'">
          <el-button type="primary" @click="editExamTime(scope.row)">修改</el-button>
          <el-button type="primary" @click="pushExam(scope.row)">开放</el-button>
          <el-button type="primary" @click="lookExam(scope.row)">查看</el-button>

        </div>

        <el-dialog title="修改起始、截至日期" :visible.sync="dialogVisible">
          <el-date-picker
              v-model="edit_start_time"
              type="datetime"
              placeholder="选择开始日期"
              style="margin-bottom: 15px; width: 50%">
          </el-date-picker>
          <br />
          <el-date-picker
              v-model="edit_end_time"
              type="datetime"
              placeholder="选择截止日期"
              style="margin-bottom: 15px; width: 50%">
          </el-date-picker>
          <br />
          <br />
          <el-button @click="submitEditExam" type="primary">确认</el-button>
        </el-dialog>

      </template>
    </el-table-column>

  </el-table>
</template>

<script>
export default {
  name: "checkExam",
  data(){
    return{
      examList:[],
      class_id :"",
      dialogVisible : false,
      edit_start_time : null,
      edit_end_time : null,
      edit_exam_id : null
    }
  },
  methods: {
    getExamList(){
      this.axios.post("/api/getExam",JSON.stringify({
        class_id : this.class_id,
        token : sessionStorage.getItem('token')
      })).then((res)=>{
        if(res.data.code === 200){
          this.examList = []
          if(res.data.data.role !== 2){
            this.$router.push({
              path: '/404',
            });
          }
          for(var i = 0; i<res.data.data.data.length; i++){
            if(res.data.data.data[i].status === 0){
              res.data.data.data[i].status = "未开放"
              res.data.data.data[i].type = "warning"
            }
            else if(res.data.data.data[i].status === 1){
              res.data.data.data[i].status = "进行中"
              res.data.data.data[i].type = "success"
            }
            else{
              res.data.data.data[i].status = "已截止"
              res.data.data.data[i].type = "danger"
            }

            this.examList.push(res.data.data.data[i])
          }
        }
      })
    },
    getParams(){
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))["class_id"];
    },
    pushExam(row){
      this.axios.post("/api/pushExam",JSON.stringify({
        exam_id : row.exam_id
      })).then((res)=>{
        if(res.data.code === 200){
          this.getExamList()
        }
      })
    },
    lookExam(row){
      this.$router.push({
        path: '/teacherHome/concreteCourse/exam',
        query: {info: this.$Base64.encode(JSON.stringify({ exam_id: row.exam_id })),},
      });
    },
    stopExam(row){
      this.axios.post("/api/stopExam",JSON.stringify({
        exam_id : row.exam_id
      })).then((res)=>{
        console.log(res)
        if(res.data.code === 200){
          this.getExamList()
        }
      })

    },
    editExamTime(row){
      this.dialogVisible = true
      this.edit_exam_id = row.exam_id
    },
    submitEditExam(){
      this.dialogVisible = false;
      this.axios.post("/api/editExamTime",JSON.stringify({
        exam_id : this.edit_exam_id,
        start_time : this.formatDateTime(this.edit_start_time),
        end_time : this.formatDateTime(this.edit_end_time)
      })).then((res)=>{
        if(res.data.code === 200){
          this.$message("修改成功！")
          this.getExamList()
        }
        else{
          this.$message("修改失败")
        }
        this.edit_start_time = null
        this.edit_end_time = null
        this.edit_exam_id = null
      })
    },
    formatDateTime(date) {
      //时间戳转换
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      var d = date.getDate();
      d = d < 10 ? "0" + d : d;
      var h = date.getHours();
      h = h < 10 ? "0" + h : h;
      var minute = date.getMinutes();
      minute = minute < 10 ? "0" + minute : minute;
      var second = date.getSeconds();
      second = second < 10 ? "0" + second : second;
      return y + "-" + m + "-" + d + " " + h + ":" + minute + ":" + second;
    },
  },
  mounted() {
    this.getParams();
    this.getExamList();
  }
}
</script>

<style scoped>
.el-button--primary{
  color: white;
}
</style>
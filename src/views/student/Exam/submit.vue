<template>
<div style="text-align: center;">
  <el-progress type="circle" :percentage="100" status="success"></el-progress>
  <br />
  <br />
  <h3>
    提交成功！
  </h3>
  <br />
  <br />
  <h3>
    您的得分是：<el-tag>{{score}}</el-tag>
  </h3>
  <br />
  <br />
  <h3>
    您的组内排名是：<el-tag>{{rank}}</el-tag>
  </h3>

  <br />
  <br />
  <h3>组内成员</h3>
  <el-table
      :data="group"
      border
      style="width: 100%">
    <el-table-column
        prop="id"
        label="学号"
        width="400">
    </el-table-column>
    <el-table-column
        prop="name"
        label="姓名"
        width="400">
    </el-table-column>
    <el-table-column
        prop="score"
        label="得分">
    </el-table-column>
  </el-table>

</div>
</template>

<script>
export default {
  name: "submit",
  data(){
    return{
      exam_id:"",
      class_id:"",
      score:"",
      rank:"",
      group:[]
    }
  },
  methods:{
    lookExam() {
      this.$router.push({
        path: "/studentHome/concreteCourse/examHome/checkExam",
        query: {
          info: this.$Base64.encode(
              JSON.stringify({ class_id: this.class_id })
          ),
        },
      });
    },
    getParams() {
      this.exam_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
          "exam_id"
          ];
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
          "class_id"
          ];
      this.score = JSON.parse(this.$Base64.decode(this.$route.query.info))[
          "score"
          ];
      this.rank = JSON.parse(this.$Base64.decode(this.$route.query.info))[
          "rank"
          ];
    },
    getGroup(){
      this.axios.post("/api/getExamGroupById",JSON.stringify({
        exam_id:this.exam_id,
        s_id:sessionStorage.getItem("id")
      })).then((res)=>{
        if(res.data.code === 200){
          this.group = res.data.data
        }
        else{
          this.$message("网络错误！")
        }
      }).catch((err)=>{
        this.$message("网络错误！")
        console.log(err)
      })
    }
  },
  mounted() {
    this.getParams()
    this.getGroup()
  }
}
</script>

<style scoped>

</style>

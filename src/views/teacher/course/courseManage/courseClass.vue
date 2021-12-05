<template>
  <div>
    <el-container>
      <el-aside width="50%">
        <v-btn
          color="primary"
          dark
          style="margin-left: 1%; margin-top: 1%; margin-bottom: 1%" @click="createClass">
          新增班级
        </v-btn>
        <el-scrollbar>
          <v-row dense>
            <v-col v-for="(item, i) in classList" :key="i" cols="12">
              <v-card color="#385F73" dark>
                <div>
                  <v-card-title
                    class="text-h5"
                    v-text="item.name + '\t' + item.class_id "
                  >
                  </v-card-title>
                  <v-card-text
                      v-text=" '教师工号：' + item.t_id + '\t' + '教师姓名：' + item.t_name ">
                  </v-card-text>
                  <v-card-subtitle v-text="item.respondTea"></v-card-subtitle>

                  <v-card-actions>
                    <v-btn outlined rounded @click="handleTea">
                      设置教师
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn text @click="handleDeleteClass(item)">
                      删除班级
                    </v-btn>
                  </v-card-actions>
                </div>
              </v-card>
              <el-dialog
                :visible.sync="teaDialog"
                title="选择教师"
                center
                width="300px"
              >
                <el-autocomplete
                  v-model="item.tid"
                  placeholder="请输入教师id"
                  :fetch-suggestions="querySearchAsync"
                  value-key="tid"
                  autocomplete="off"
                  style="margin-letf: 20%"
                  margin-left="20px"
                ></el-autocomplete>

                <div slot="footer" class="dialog-footer">
                  <el-button @click="teaDialog = false">取消</el-button>
                  <el-button type="primary" @click="addTea(item)"
                    >确定</el-button
                  >
                </div>
              </el-dialog>
            </v-col>
          </v-row>
        </el-scrollbar>
      </el-aside>

      <el-main>
        <el-scrollbar>
          <el-row>
            <el-col :span="6">
              <v-btn dark @click="saveInfo()">保存课程信息</v-btn></el-col
            >
            <el-col :span="6">
              <v-btn dark @click="handleFile">上传教学大纲</v-btn></el-col
            >
            <el-col :span="3"> <v-btn dark>新增实验</v-btn></el-col></el-row
          >
          <el-descriptions
            :column="1"
            border
            style="margin-bottom: 10px; margin-top: 10px"
            title="课程信息"
          >
            <el-descriptions-item label="课程id"
              >kooriookami</el-descriptions-item
            >
            <el-descriptions-item label="课程名称"
              >18100000000</el-descriptions-item
            >
            <el-descriptions-item label="责任教师" :span="2"
              >苏州市</el-descriptions-item
            >
            <el-descriptions-item label="上课时间">
              <el-tag size="small">学校</el-tag>
            </el-descriptions-item>
          </el-descriptions>
          <v-textarea v-model="syllabus" color="white" label="课程简介" filled>
          </v-textarea>

          <v-row dense>
            <v-col v-for="(item, i) in experList" :key="i" cols="6">
              <v-card color="#1F7087" dark>
                <v-card-title v-text="item.title"></v-card-title>

                <v-card-subtitle v-text="'占比:' + item.weight"> </v-card-subtitle>

                <v-card-actions>
                  <v-btn text @click="handleProportion"> 设置占比 </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn text @click="handleDeleteExper(item)">
                    删除实验
                  </v-btn>
                </v-card-actions>
              </v-card>
              <el-dialog
                :visible.sync="proDialog"
                title="设置实验占比"
                center
                width="300px"
              >
                <el-input v-model="item.proportion"></el-input>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="proDialog = false">取消</el-button>
                  <el-button type="primary" @click="setPro(item.proportion)"
                    >确定</el-button
                  >
                </div>
              </el-dialog>
            </v-col>
          </v-row>
        </el-scrollbar>

        <el-dialog :visible.sync="fileDialog" title="请选择文件" center>
          <el-upload
            class="upload-import"
            ref="uploadImport"
            action="https://baidu.com/"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :on-change="handleChange"
            :before-remove="beforeRemove"
            :file-list="fileList"
            :multiple="true"
            :auto-upload="false"
            accept=""
          >
            <el-button type="primary">选取文件</el-button>
          </el-upload>
          <div slot="footer" class="dialog-footer">
            <el-button @click="fileDialog = false">取消</el-button>
            <el-button type="success" @click="addFile()">上传</el-button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>

export default {
  data() {
    return {
      syllabus: "",
      teaDialog: false,
      proDialog: false,
      fileDialog: false,
      courseID:"",
      classList: [],
      experList: [],
      fileList: [],
      teacherExist: [],
      timeout: null,
    };
  },
  methods: {
    handlePreview(file) {
      console.log(file);
    },

    handleRemove(file, fileListS) {
      console.log(file, fileListS);
    },

    handleChange(file) {
      console.log(file);
      this.fileListS.push(file);
      console.log(this.fileListS);
    },

    beforeRemove(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },
    saveInfo() {},
    handleTea() {
      this.teaDialog = true;
    },
    handleProportion() {
      this.proDialog = true;
    },
    handleFile() {
      this.fileDialog = true;
    },
    addTea(row) {
      console.log(row);
      if (this.isExist(row.tid)) {
        this.teaDialog = false;
      } else {
        this.$message("没有这个老师！");
        this.teaDialog = true;
      }
    },
    setPro(row) {
      console.log(row);
      this.proDialog = false;
    },
    addFile() {},
    isExist(row) {
      console.log("row===" + row);
      console.log(this.teacherExist);
      var ret = this.teacherExist.indexOf(row);
      console.log("ret===" + ret);
      return ret > 0;
    },

    querySearchAsync(queryString, cb) {
      var teacherExist = this.teacherExist;
      var results = queryString
        ? teacherExist.filter(this.createStateFilter(queryString))
        : teacherExist;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 3000 * Math.random());
    },

    createStateFilter(queryString) {
      return (data) => {
        return data.tid.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
      };
    },

    handleDeleteClass(item) {
      this.$confirm("确认删除班级吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.axios.post("/api/manageClass/deleteClass",JSON.stringify({
            classID : item.class_id
          })).then()
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          this.getClasses()
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },
    createClass(){
      this.axios.post('/api/addClass/'),JSON.stringify({
        courseID:this.courseID
      }).then((response) => {
        console.log(response)
      })
    },
    getClasses(){
      this.axios.post('/api/manageClass/showClass/',JSON.stringify({
        courseID : this.courseID
      })).then((response) => {
        console.log(response.data)
        this.classList = response.data
      });
    },
    handleDeleteExper(item) {
      this.$confirm("确认删除实验吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.axios.post("/api/course/delEx/",JSON.stringify({
            ex_id : item.ex_id
          })).then(() => {
            this.$message({
              type: "success",
              message: "删除成功!",
            });
            this.getExper()
          })

        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },
    getExper(){
      this.axios.post('/api/course/getEx/',JSON.stringify({
        c_id : this.courseID
      })).then((response) => {
        console.log(response.data)
        this.experList = response.data
      });
    }
  },
  mounted() {
    this.courseID = JSON.parse(this.$Base64.decode(this.$route.query.info))['courseID']
    this.getClasses();
    this.getExper()
  },
};
</script>

<style scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
  overflow-y: hidden;
}
</style>
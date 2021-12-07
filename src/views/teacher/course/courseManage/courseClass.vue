<template>
  <div>
    <el-container>
      <el-aside width="50%">
        <v-btn
          color="primary"
          dark
          style="margin-left: 1%; margin-top: 1%; margin-bottom: 1%"
          @click="handleAddClass"
        >
          新增班级
        </v-btn>

        <el-scrollbar>
          <v-row dense>
            <v-col v-for="item in classList" :key="item.class_id" cols="12">
              <v-card color="#385F73" dark>
                <div>
                  <v-card-title
                    class="text-h5"
                    v-text="item.class_id"
                  ></v-card-title>
                  <v-card-subtitle v-text="item.t_name"></v-card-subtitle>
                  <v-card-actions>
                    <v-btn outlined rounded @click="handleTea(item)">
                      设置教师
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn text @click="handleDeleteClass(item)">
                      删除班级
                    </v-btn>
                  </v-card-actions>
                </div>
              </v-card>
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
            <el-col :span="3">
              <v-btn dark @click="handleAddEx">新增实验</v-btn></el-col
            >
          </el-row>
          <el-descriptions
            :column="1"
            border
            style="margin-bottom: 10px; margin-top: 10px"
            title="课程信息"
          >
            <el-descriptions-item label="课程id">{{
              courseID
            }}</el-descriptions-item>
            <el-descriptions-item label="课程名称">{{
              name
            }}</el-descriptions-item>
            <el-descriptions-item label="责任教师" :span="2">{{
              id
            }}</el-descriptions-item>
            <el-descriptions-item label="上课时间">
              {{ year }}年 {{ semester }}
            </el-descriptions-item>
          </el-descriptions>

          <v-row dense>
            <v-col v-for="item in experList" :key="item.ex_id" cols="6">
              <v-card color="#1F7087" dark>
                <div>
                  <v-card-title v-text="item.title"></v-card-title>
                  <v-card-subtitle
                    v-text="'实验占比：' + item.weight"
                  ></v-card-subtitle>
                  <v-card-subtitle
                      v-text="'实验状态：' + item.status"
                  ></v-card-subtitle>
                  <v-card-text
                    v-text="'截止日期：' + item.end_time"
                  ></v-card-text>
                  <v-card-actions>
                    <v-btn text @click="handleProportion(item)">
                      设置占比
                    </v-btn>
                    <v-btn text @click="handlePushExper(item)">
                      发布实验
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn text @click="handleDeleteExper(item)">
                      删除实验
                    </v-btn>
                  </v-card-actions>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </el-scrollbar>

        <el-dialog
          :visible.sync="classDialog"
          title="新增班级"
          center
          width="300px"
        >
          <el-select v-model="tid">
            <el-option
              v-for="item in teaList"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            >
            </el-option>
          </el-select>

          <div slot="footer" class="dialog-footer">
            <el-button @click="classDialog = false">取消</el-button>
            <el-button type="primary" @click="createClass()">确定</el-button>
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="teaDialog"
          title="选择教师"
          center
          width="300px"
        >
          <el-select v-model="changeTemp.t_id">
            <el-option
              v-for="i in teaList"
              :key="i.id"
              :label="i.id"
              :value="i.id"
            >
            </el-option>
          </el-select>
          <div slot="footer" class="dialog-footer">
            <el-button @click="teaDialog = false">取消</el-button>
            <el-button type="primary" @click="updateTea(changeTemp)"
              >确定</el-button
            >
          </div>
        </el-dialog>

        <el-dialog
          :visible.sync="proDialog"
          title="设置实验占比"
          center
          width="300px"
        >
          <el-input v-model="changeTemp.weight"></el-input>
          <div slot="footer" class="dialog-footer">
            <el-button @click="proDialog = false">取消</el-button>
            <el-button type="primary" @click="setPro(changeTemp)"
              >确定</el-button
            >
          </div>
        </el-dialog>

        <el-dialog :visible.sync="exDialog" title="新增实验" center width="70%">
          <v-container>
            <v-row style="margin-bottom: 5px">
              <v-col cols="6">
                <el-date-picker
                  v-model="experiment.end_time"
                  type="datetime"
                  placeholder="选择实验截止日期时间"
                  :picker-options="pickerOptions"
                  style="margin-bottom: 15px; width: 100%"
                >
                </el-date-picker>
              </v-col>
              <v-col cols="6">
                <el-select
                  v-model="experiment.status"
                  placeholder="请选择实验提交方式"
                  style="margin-bottom: 15px; width: 100%"
                >
                  <el-option
                    v-for="item in exStatus"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </v-col>
            </v-row>

            <v-textarea
              filled
              label="实验名称"
              auto-grow
              height="20px"
              v-model="experiment.title"
            ></v-textarea>

            <v-textarea
              filled
              label="实验简介"
              auto-grow
              v-model="experiment.brief"
            ></v-textarea>

            <v-textarea
              filled
              label="实验占比"
              auto-grow
              height="20px"
              v-model="experiment.weight"
            ></v-textarea>
          </v-container>

          <div slot="footer" class="dialog-footer">
            <el-button @click="exDialog = false">取消</el-button>
            <el-button type="primary" @click="addEx()">确定</el-button>
          </div>
        </el-dialog>

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
      classDialog: false,
      exDialog: false,

      courseID: "",
      name: "",
      year: "",
      semester: "",
      id: "",

      tid: "",
      teaList: [],
      classList: [],
      experList: [],
      fileList: [],
      experiment: {
        courseID: "",
        title: "",
        brief: "",
        weight: "",
        end_time: "",
        status: null,
      },
      exStatus: [
        {
          value: "在线提交",
          label: "在线提交",
        },
        {
          value: "在线提交",
          label: "提交文件",
        },
      ],

      changeTemp: {},
      timeout: null,
      pickerOptions: {
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            },
          },
          {
            text: "明天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24);
              picker.$emit("pick", date);
            },
          },
          {
            text: "一周后",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            },
          },
        ],
      },
    };
  },
  methods: {
    getParams: function () {
      this.courseID = this.$route.query.c_id;
      this.name = this.$route.query.name;
      this.year = this.$route.query.year;
      this.semester = this.$route.query.semester;
      this.id = sessionStorage.getItem("id");
      this.experiment.courseID = this.$route.query.c_id;
    },
    handlePushExper(item){
      this.axios.post("/api/course/pushEx/",JSON.stringify({
        ex_id : item.ex_id
      })).then(()=>{
        this.$message("发布成功！")
        this.getExperiment()
      })
    },
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
    handleTea(item) {
      this.changeTemp = item;
      this.teaDialog = true;
    },
    handleProportion(item) {
      this.changeTemp = item;
      this.proDialog = true;
    },
    handleFile() {
      this.fileDialog = true;
    },
    handleAddClass() {
      this.classDialog = true;
    },
    handleAddEx() {
      this.exDialog = true;
    },
    handleDeleteClass(row) {
      this.$confirm("确认删除班级吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteClass(row);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          document.execCommand("Refresh");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },
    handleDeleteExper(item) {
      this.$confirm("确认删除实验吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteEx(item);
          this.$message({
            type: "success",
            message: "删除成功!",
          });
          document.execCommand("Refresh");
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除操作",
          });
        });
    },

    updateTea(row) {
      var jsons = {
        class_id: row.class_id,
        t_id: row.t_id,
      };
      console.log("更新教师");
      console.log(jsons);
      this.axios
        .post("/api/manageClass/changeTeacher", JSON.stringify(jsons))
        .then((response) => {
          console.log(response.data);
          this.getClasses();
          this.teaDialog = false;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setPro(row) {
      var jsons = {
        title: row.title,
        brief: row.brief,
        end_time: "2021-12-1 17:00:00",
        ex_id: row.ex_id,
        status: row.status,
        weight: row.weight,
      };
      console.log("更新占比");
      console.log(jsons);

      this.axios
        .post("/api/course/editEx/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response.data);
          this.getExperiment();
          this.proDialog = false;
        })
        .catch(function (error) {
          console.log(error);
        });
      this.getExperiment();
    },
    addFile() {},
    createClass() {
      this.axios
        .post(
          "/api/manageClass/addClass",
          JSON.stringify({
            courseID: this.courseID,
            t_id: this.tid,
          })
        )
        .then((response) => {
          console.log(response);
          this.classDialog = false;
          this.tid = "";
          this.getClasses();
        });
    },
    deleteClass(row) {
      var jsons = {
        classID: row.class_id,
      };
      this.axios
        .post("/api/manageClass/deleteClass", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          this.getClasses();
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    addEx() {
      var jsons = {
        courseID: this.experiment.courseID,
        title: this.experiment.title,
        brief: this.experiment.brief,
        weight: this.experiment.weight,
        end_time: this.formatDateTime(this.experiment.end_time),
        ex_type: this.experiment.status,
      };
      console.log("新增实验");
      console.log(jsons);

      this.axios
        .post("/api/course/addEx/", JSON.stringify(jsons))
        .then((response) => {
          if(response.data === "WeightUnreasonable"){
            this.$message("权重不合理！");
          }
          else{
            this.$message("添加成功！");
          }
          this.exDialog = false;
          this.getExperiment();
        });
    },
    deleteEx(item) {
      var jsons = {
        ex_id: item.ex_id,
      };
      this.axios
        .post("/api/course/delEx/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          this.getExperiment();
        })
        .catch(function (error) {
          console.log(error);
        });
    },

    getClasses() {
      var jsons = {
        courseID: this.courseID,
      };
      this.axios
        .post("/api/manageClass/showClass/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response.data);
          this.classList = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });

      /*this.axios({
        method: "get",
        url: "/api/showClass/",
        crossDomain: true,
        data: JSON.stringify(jsons),
      })
        .then((response) => {
          console.log(response);
          // this.classList = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });*/
    },
    getExperiment() {
      var jsons = {
        c_id: this.courseID,
      };
      this.axios
        .post("/api/course/getEx/", JSON.stringify(jsons))
        .then((response) => {
          console.log(response)
          this.experList = response.data;
          for(var i = 0; i < this.experList.length; i++){
            if(this.experList[i].status === 0){
              this.experList[i].status = "未发布"
            }
            else if(this.experList[i].status === 1){
              this.experList[i].status = "已发布"
            }
            else{
              this.experList[i].status = "已过期"
            }
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    getTeaList() {
      //获得所有教师
      this.axios
        .get("/api/course/getAllTeacher/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => {
          this.teaList = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
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
    this.getClasses();
    this.getExperiment();
    this.getTeaList();
  },
};
</script>

<style scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
  overflow-y: hidden;
}
</style>
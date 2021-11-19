<template>
  <div>
    <el-container>
      <el-aside width="600px">
        <el-scrollbar>
          <v-row dense>
            <v-col v-for="(item, i) in items" :key="i" cols="12">
              <v-card color="#385F73" dark>
                <div class="d-flex flex-no-wrap justify-space-between">
                  <v-card-title
                    class="text-h5"
                    v-text="item.title"
                  ></v-card-title>

                  <v-card-subtitle v-text="item.respondTea"></v-card-subtitle>

                  <v-card-actions>
                    <v-btn
                      class="ml-2 mt-5"
                      outlined
                      rounded
                      @click="handleTea"
                    >
                      设置责任教师
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
            <el-col :span="3">
              <v-btn dark @click="saveInfo()">保存</v-btn></el-col
            >
            <el-col :span="3">
              <v-btn dark @click="handleFile">上传教学大纲</v-btn></el-col
            ></el-row
          >
          <el-descriptions
            :column="1"
            border
            style="margin-bottom: 10px; margin-top: 10px"
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
          <v-textarea v-model="syllabus" color="teal" label="教学大纲" filled>
          </v-textarea>
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
      fileDialog: false,
      items: [
        {
          title: "Supermodel",
          respondTea: "Foster the People",
          tid: "1",
        },
        {
          title: "班级",
          respondTea: "责任教师",
          tid: "2",
        },
      ],
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
    handleFile() {
      this.fileDialog = true;
    },
    addTea(row) {
      console.log(row);
      if (this.isExist(row.tid)) {
        this.dialogVisible = false;
      } else {
        this.$message("没有这个老师！");
        this.dialogVisible = true;
      }
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

    loadAll() {
      return [
        { tid: "三全鲜食（北新泾店）" },
        {
          tid: "Hot honey 首尔炸鸡（仙霞路）",
        },
        {
          tid: "2",
        },
      ];
    },
  },
  mounted() {
    this.teacherExist = this.loadAll();
  },
};
</script>

<style scoped>
.el-scrollbar__wrap {
  overflow-x: hidden;
  overflow-y: hidden;
}
</style>
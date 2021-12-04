<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="所有人" name="first">
        <el-row>
          <el-col :span="3">
            <v-btn dark @click="handleDetailS">手动添加学生</v-btn></el-col
          >
          <el-col :span="3" :offset="1"
            ><v-btn dark @click="handleExcelS">表格导入学生</v-btn></el-col
          ><el-col :span="5" :offset="10">
            <v-text-field
              v-model="assist"
              :append-outer-icon="isRead ? 'mdi-pencil' : 'mdi-send'"
              filled
              label="助教"
              type="text"
              :readonly="isRead"
              @click:append-outer="changeAssist"
            ></v-text-field></el-col
        ></el-row>

        <el-table
          :data="
            studentData.filter(
              (data) =>
                !searchP ||
                data.name.toLowerCase().includes(searchP.toLowerCase()) ||
                data.id.toLowerCase().includes(searchP.toLowerCase()) ||
                data.role.toLowerCase().includes(searchP.toLowerCase())
            )
          "
          style="width: 100%"
        >
          <el-table-column prop="s_id" label="学号" sortable />
          <el-table-column prop="name" label="姓名" sortable />
          <el-table-column
            prop="role"
            label="身份"
            sortable
            :filters="[
              { text: '学生', value: 1 },

              { text: '助教', value: 2 },
            ]"
            :filter-method="filterIdentity"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.role === 1">学生</span>

              <span v-if="scope.row.role === 2">助教</span>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="小组" name="second">
        <el-row>
          <el-col :span="3">
            <v-btn dark @click="handleDetailG">手动添加小组</v-btn></el-col
          >
          <el-col :span="3" :offset="1"
            ><v-btn dark @click="handleExcelT">表格导入小组</v-btn></el-col
          ></el-row
        >

        <v-expansion-panels focusable style="margin-top: 20px">
          <v-expansion-panel v-for="(data, index) in groupData" :key="index">
            <v-expansion-panel-header>
              {{ data.leader }}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <div v-for="(data, index) in data.member" :key="index">
                {{ data.name }}
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </el-tab-pane>
    </el-tabs>
    <el-dialog :visible.sync="dialogFormVisibleS" title="请输入学生信息" center>
      <el-form
        :model="formS"
        ref="formS"
        style="margin: 40px 65px 0px 25px"
        label-width="80px"
      >
        <el-form-item
          label="姓名"
          :required="true"
          prop="name"
          status-icon="true"
        >
          <el-input v-model="formS.name" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item
          label="学号"
          :required="true"
          prop="id"
          status-icon="true"
        >
          <el-input v-model="formS.id"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisibleS = false">取消</el-button>
        <el-button type="primary" @click="addFromDetailS()">确定</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogFormVisibleG"
      title="请输入小组成员信息"
      center
    >
      <el-form
        ref="dynamicValidateForm"
        :model="dynamicValidateForm"
        style="margin: 40px 65px 0px 25px"
        label-width="80px"
        class="demo-dynamic"
      >
        <el-form-item
          prop="leader"
          label="组长"
          :rules="{
            required: true,
            message: 'id can not be null',
            trigger: 'blur',
          }"
        >
          <el-input v-model="dynamicValidateForm.leader"></el-input>
        </el-form-item>
        <el-form-item
          v-for="(domain, index) in dynamicValidateForm.members"
          :key="domain.key"
          :label="'学生' + index"
          :prop="'members.' + index + '.sid'"
          :rules="{
            required: true,
            message: 'id can not be null',
            trigger: 'blur',
          }"
        >
          <el-input v-model="domain.sid"></el-input
          ><el-button @click.prevent="removeDomain(domain)">移除</el-button>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="addFromDetailT('dynamicValidateForm')"
            >确定</el-button
          >
          <el-button @click="addDomain">新成员</el-button>
          <el-button @click="dialogFormVisibleG = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :visible.sync="dialogExcelVisibleS" title="请选择文件" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileListS"
        :multiple="true"
        :auto-upload="false"
        accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
      >
        <el-button type="primary">选取文件</el-button>
        <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogExcelVisibleS = false">取消</el-button>
        <el-button type="success" @click="addFromExcelS()">上传</el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogExcelVisibleG" title="请选择文件" center>
      <el-upload
        class="upload-import"
        ref="uploadImport"
        action="https://baidu.com/"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-change="handleChange"
        :before-remove="beforeRemove"
        :file-list="fileListG"
        :multiple="true"
        :auto-upload="false"
        accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
      >
        <el-button type="primary">选取文件</el-button>
        <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogExcelVisibleG = false">取消</el-button>
        <el-button type="success" @click="addFromExcelG()">上传</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
      dialogFormVisibleS: false,
      dialogExcelVisibleS: false,
      dialogFormVisibleG: false,
      dialogExcelVisibleG: false,

      studentData: [],
      groupData: [],
      class_id : "",

      assist: "111",
      isRead: true,

      /*手动导入学生数据*/
      formS: {
        name: "",
        id: "",
      },
      /*手动导入小组成员数据*/
      dynamicValidateForm: {
        members: [
          {
            key: 1,
            sid: "",
          },
        ],
        leader: "",
      },
      fileListS: [],
      fileListG: [],

      currentPage: 1,
      pagesize: 6,
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    filterIdentity(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
    handleDetailS() {
      this.dialogFormVisibleS = true;
    },

    handleExcelS() {
      this.dialogExcelVisibleS = true;
    },

    handleDetailG() {
      this.dialogFormVisibleG = true;
    },

    handleExcelT() {
      this.dialogExcelVisibleG = true;
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

    addFromDetailS() {
      console.log(this.formS);
      //手动增加学生
      this.axios.post("", JSON.stringify(this.formS)).then((response) => {
        //这里使用了ES6的语法
        console.log(response); //请求成功返回的数据
      });
      this.dialogFormVisibleS = false;
      location.reload();
    },

    addFromDetailT(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert("submit!");
          this.axios
            .post("", JSON.stringify(this.dynamicValidateForm))
            .then((response) => {
              //这里使用了ES6的语法
              console.log(response); //请求成功返回的数据
            });
          this.dialogFormVisibleG = false;
          //location.reload();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },

    addFromExcelS() {
      /*let fdParams = new FormData();
      this.fileListS.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      fdParams.append("userID", "123");

      this.axios
        .post("/api/file/addUser/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          timeout: 20000,
        })
        .then((response) => {
          console.log(response);
        })
        .catch({});

      this.dialogExcelVisibleS = false;*/
    },

    addFromExcelG() {
      /*let fdParams = new FormData();
      this.fileListG.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      fdParams.append("userID", "123");

      this.axios
        .post("/api/file/addUser/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          timeout: 20000,
        })
        .then((response) => {
          console.log(response);
        })
        .catch({});

      this.dialogExcelVisibleG = false;*/
    },
    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },

    changeAssist() {
      if (!this.isRead) {
        this.setAssist;
        location.reload();
      } else this.isRead = !this.isRead;
    },

    setAssist() {
      //上传助教
    },
    removeDomain(item) {
      const index = this.dynamicValidateForm.members.indexOf(item);
      if (index !== -1) {
        this.dynamicValidateForm.members.splice(index, 1);
      }
    },
    addDomain() {
      this.dynamicValidateForm.members.push({
        key: Date.now(),
        sid: "",
      });
    },
  },
  mounted() {
    this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))['class_id'];
    this.axios.post(
        "/api/manageClass/IDGetClassStudent",JSON.stringify(
            {
              class_id : this.class_id,
            }),
    ).then((response) => {
      //这里使用了ES6的语法
      //this.tableData = response.data
      this.studentData = response.data['data']
      //this.checkResponse(response.data); //请求成功返回的数据
    })
  }
};
</script>

<style scoped>
.box-card {
  border-radius: 15px;
  box-shadow: 7px 7px 10px rgba(0, 0, 0, 0.15);
}
.el-card {
  margin-bottom: 20px;
  margin-top: 15px;
}
</style>
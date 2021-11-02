<template>
  <div>
    <el-card>
      <el-button type="info" @click="checkData()">check</el-button>

      <el-button type="info" @click="handleDetailS">手动添加学生</el-button>
      <el-button type="info" @click="handleDetailT">手动添加教师</el-button>
      <el-button type="info" @click="handleExcelS">表格导入学生</el-button>
      <el-button type="info" @click="handleExcelT">表格导入老师</el-button>
      <el-dialog
        :visible.sync="dialogFormVisibleS"
        title="请输入学生信息"
        center
      >
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

          <el-form-item
            label="邮箱"
            prop="email"
            status-icon="true"
            :required="true"
          >
            <el-input type="email" v-model="formS.email"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisibleS = false">取消</el-button>
          <el-button type="primary" @click="addFromDetailS()">确定</el-button>
        </div>
      </el-dialog>

      <el-dialog
        :visible.sync="dialogFormVisibleT"
        title="请输入教师信息"
        center
      >
        <el-form
          :model="formT"
          ref="formT"
          style="margin: 40px 65px 0px 25px"
          label-width="80px"
        >
          <el-form-item
            label="姓名"
            :required="true"
            prop="name"
            status-icon="true"
          >
            <el-input v-model="formT.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item
            label="工号"
            :required="true"
            prop="id"
            status-icon="true"
          >
            <el-input v-model="formT.id"></el-input>
          </el-form-item>

          <el-form-item
            label="邮箱"
            prop="email"
            status-icon="true"
            :required="true"
          >
            <el-input type="email" v-model="formT.email"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisibleT = false">取消</el-button>
          <el-button type="primary" @click="addFromDetailT()">确定</el-button>
        </div>
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

      <el-dialog :visible.sync="dialogExcelVisibleT" title="请选择文件" center>
        <el-upload
          class="upload-import"
          ref="uploadImport"
          action="https://baidu.com/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-change="handleChange"
          :before-remove="beforeRemove"
          :file-list="fileListT"
          :multiple="true"
          :auto-upload="false"
          accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        >
          <el-button type="primary">选取文件</el-button>
          <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogExcelVisibleT = false">取消</el-button>
          <el-button type="success" @click="addFromExcelT()">上传</el-button>
        </div>
      </el-dialog>

      <el-table
        ref="filterTable"
        row-key="id"
        :data="
          userData.slice((currentPage - 1) * pagesize, currentPage * pagesize)
        "
        style="width: 100%"
      >
        <el-table-column prop="name" label="姓名" sortable />
        <el-table-column prop="id" label="学号" sortable />
        <el-table-column
          prop="role"
          label="身份权限"
          sortable
          :filters="[
            { text: '学生', value: 1 },

            { text: '教师', value: 2 },
          ]"
          :filter-method="filterIdentity"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.role === 1">学生</span>

            <span v-if="scope.row.role === 2">教师</span>
          </template>
        </el-table-column>

        <el-table-column
          prop="is_active"
          label="状态"
          sortable
          :filters="[
            { text: '激活', value: 1 },
            { text: '非激活', value: 0 },
          ]"
          :filter-method="filterState"
          filter-placement="bottom-end"
        >
          <template #default="scope">
            <el-tag
              :type="scope.row.is_active === 1 ? 'success' : 'danger'"
              disable-transitions
              ><span v-if="scope.row.is_active === 1">激活</span>
              <span v-if="scope.row.is_active === 0">非激活</span></el-tag
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="userData.length"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script >
import axios from "axios";

export default {
  data() {
    return {
      dialogFormVisibleS: false,
      dialogExcelVisibleS: false,
      dialogFormVisibleT: false,
      dialogExcelVisibleT: false,

      /*手动导入学生数据*/
      formS: {
        name: "",
        id: "",
        email: "",
      },
      /*手动导入教师数据*/
      formT: {
        name: "",
        id: "",
        email: "",
      },

      /**/

      fileListS: [],
      fileListT: [],

      currentPage: 1,
      pagesize: 6,
      userData: [],
    };
  },
  methods: {
    handleDetailS() {
      this.dialogFormVisibleS = true;
    },

    handleExcelS() {
      this.dialogExcelVisibleS = true;
    },

    handleDetailT() {
      this.dialogFormVisibleT = true;
    },

    handleExcelT() {
      this.dialogExcelVisibleT = true;
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
      axios
        .post("/api/Register/addStudentManually/", JSON.stringify(this.formS))
        .then((response) => {
          //这里使用了ES6的语法
          console.log(response); //请求成功返回的数据
        });
      this.dialogFormVisibleS = false;
      location.reload();
    },

    addFromDetailT() {
      this.axios
        .post("/api/Register/addTeacherManually/", JSON.stringify(this.formT))
        .then((response) => {
          //这里使用了ES6的语法
          console.log(response); //请求成功返回的数据
        });
      this.dialogFormVisibleT = false;
      location.reload();
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

    addFromExcelT() {
      /*let fdParams = new FormData();
      this.fileListT.forEach((file) => {
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

      this.dialogExcelVisibleT = false;*/
    },

    handleSizeChange: function (val) {
      this.pagesize = val;
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
    },
    filterState(value, row) {
      return row.state === value;
    },
    filterIdentity(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },

    checkData() {
      console.log(this.userData);
    },
  },
  mounted() {
    //获取所有用户所有信息
    axios
      .get("/api/getUserInfo/allUser/", {
        //params: { userData: "value" },
        crossDomain: true,
      })
      .then((response) => (this.userData = response.data))
      .catch(function (error) {
        console(error);
      });
  },
};
</script>

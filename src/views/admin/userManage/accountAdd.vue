<template>
  <div>
    <el-card>
      <el-dropdown @command="handleCommandDetail" style="margin-right: 10px">
        <el-button type="info" style="background: #7986cb; color: white">
          手动添加<i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="s">添加学生</el-dropdown-item>
          <el-dropdown-item command="t">添加老师</el-dropdown-item>
          <el-dropdown-item command="a">添加助教</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>

      <el-dropdown @command="handleCommandForm" style="margin-right: 10px">
        <el-button type="info" style="background: #7986cb; color: white">
          表格导入<i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="s">导入学生</el-dropdown-item>
          <el-dropdown-item command="t">导入老师</el-dropdown-item>
          <el-dropdown-item command="a">导入助教</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>

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
            :rules="nameRules"
            prop="name"
            status-icon="true"
          >
            <el-input v-model="formS.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item
            label="学号"
            :rules="idRules"
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
            :rules="nameRules"
            prop="name"
            status-icon="true"
          >
            <el-input v-model="formT.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item
            label="工号"
            :rules="idRules"
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

      <el-dialog
        :visible.sync="dialogFormVisibleA"
        title="请输入助教信息"
        center
      >
        <el-form
          :model="formA"
          style="margin: 40px 65px 0px 25px"
          label-width="80px"
        >
          <el-form-item
            label="姓名"
            :rules="nameRules"
            prop="name"
            status-icon="true"
          >
            <el-input v-model="formA.name" autocomplete="off"></el-input>
          </el-form-item>

          <el-form-item
            label="学号"
            :rules="idRules"
            prop="ta_id"
            status-icon="true"
          >
            <el-input v-model="formA.ta_id"></el-input>
          </el-form-item>

          <el-form-item
            label="邮箱"
            prop="email"
            status-icon="true"
            :required="true"
          >
            <el-input type="email" v-model="formA.email"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisibleA = false">取消</el-button>
          <el-button type="primary" @click="addFromDetailA()">确定</el-button>
        </div>
      </el-dialog>

      <el-dialog
        :visible.sync="dialogExcelVisibleS"
        title="请选择导入的学生文件"
        center
      >
        <el-upload
          class="upload-import"
          ref="uploadImport"
          action="https://baidu.com/"
          :on-preview="handlePreviewS"
          :on-remove="handleRemoveS"
          :on-change="handleChangeS"
          :before-remove="beforeRemoveS"
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
          :on-preview="handlePreviewT"
          :on-remove="handleRemoveT"
          :on-change="handleChangeT"
          :before-remove="beforeRemoveT"
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

      <el-dialog :visible.sync="dialogExcelVisibleA" title="请选择文件" center>
        <el-upload
          class="upload-import"
          ref="uploadImport"
          action="https://baidu.com/"
          :on-preview="handlePreviewTA"
          :on-remove="handleRemoveTA"
          :on-change="handleChangeTA"
          :before-remove="beforeRemoveTA"
          :file-list="fileListA"
          :multiple="true"
          :auto-upload="false"
          accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
        >
          <el-button type="primary">选取文件</el-button>
          <div slot="tip" class="el-upload__tip">只能上传excel文件</div>
        </el-upload>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogExcelVisibleA = false">取消</el-button>
          <el-button type="success" @click="addFromExcelA()">上传</el-button>
        </div>
      </el-dialog>

      <el-table
        ref="filterTable"
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
            { text: '助教', value: 3 },
          ]"
          :filter-method="filterIdentity"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.role === 1">学生</span>

            <span v-if="scope.row.role === 2">教师</span>
            <span v-if="scope.row.role === 3">助教</span>
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

        <el-table-column label="手动激活">
          <template #default="scope">
            <el-button
              plain
              @click="
                handleActive(scope.row.is_active, scope.row.id, scope.row.role)
              "
              >重新激活</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pagesize"
        layout="total,  prev, pager, next, jumper"
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
      dialogFormVisibleA: false,
      dialogExcelVisibleA: false,

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
      /*手动导入助教数据*/
      formA: {
        name: "",
        ta_id: "",
        email: "",
      },

      /**/

      fileListS: [],
      fileListT: [],
      fileListA: [],

      currentPage: 1,
      pagesize: 6,
      userData: [],

      nameRules: [
        { required: true, message: "name is required", trigger: "blur" },
      ],
      idRules: [{ required: true, message: "id is required", trigger: "blur" }],
    };
  },
  methods: {
    //重新手动激活用户
    handleActive(is_active, id, usertype) {
      if (is_active === 1) {
        this.$message("该用户已被激活，不可重新激活");
      } else {
        var jsons = {
          id: id,
          role: usertype - 1,
        };
        axios
          .post("/api/users/reActive", jsons)
          .then((response) => {
            console.log(response);
          })
          .catch(function (error) {
            console(error);
          });
        this.$message({
          message: "已发送激活邮件",
          type: "success",
        });
      }
    },

    //获取所有用户所有信息
    getUserData() {
      axios
        .get("/api/getUserInfo/allUser/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => {
          console.log("getUserData", response);
          this.userData = response.data;
          //location.reload();
        })
        .catch(function (error) {
          console(error);
        });
    },
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

    handleDetailA() {
      this.dialogFormVisibleA = true;
    },

    handleExcelA() {
      this.dialogExcelVisibleA = true;
    },

    handlePreviewS(file) {
      console.log(file);
    },

    handleRemoveS(file, fileListS) {
      console.log(file, fileListS);
    },

    handleChangeS(file) {
      console.log(file);
      this.fileListS.push(file);
      console.log(this.fileListS);
    },

    beforeRemoveS(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    handlePreviewT(file) {
      console.log(file);
    },

    handleRemoveT(file, fileListT) {
      console.log(file, fileListT);
    },

    handleChangeT(file) {
      console.log(file);
      this.fileListT.push(file);
      console.log(this.fileListT);
    },

    beforeRemoveT(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    handlePreviewTA(file) {
      console.log(file);
    },

    handleRemoveTA(file, fileListA) {
      console.log(file, fileListA);
    },

    handleChangeTA(file) {
      console.log(file);
      this.fileListA.push(file);
      console.log(this.fileListA);
    },

    beforeRemoveTA(file) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    addFromDetailS() {
      //手动增加学生
      if (
        this.formS.name != "" &&
        this.formS.id != "" &&
        this.formS.email.indexOf("@") >= 0
      ) {
        var jsons = {
          email: this.formS.email,
          id: this.formS.id,
          name: this.formS.name,
          token: sessionStorage.getItem("token"),
        };
        axios
          .post("/api/Register/addSM/", JSON.stringify(jsons))
          .then((response) => {
            console.log(" addFromDetailS", response);
            this.checkData(response.data);
            //location.reload();
          });
        this.dialogFormVisibleS = false;
        this.formS.name = "";
        this.formS.id = "";
        this.formS.email = "";
        this.getUserData();
      } else {
        this.$message({
          message: "请输入正确信息",
          type: "error",
        });
      }
      //location.reload();
    },

    addFromDetailT() {
      //手动增加教师

      if (
        this.formT.name != "" &&
        this.formT.id != "" &&
        this.formT.email.indexOf("@") >= 0
      ) {
        var jsons = {
          email: this.formT.email,
          id: this.formT.id,
          name: this.formT.name,
          token: sessionStorage.getItem("token"),
        };
        this.axios
          .post("/api/Register/addTeacherManually/", JSON.stringify(jsons))
          .then((response) => {
            this.checkData(response.data);
          });
        this.dialogFormVisibleT = false;
        this.formT.name = "";
        this.formT.id = "";
        this.formT.email = "";
        this.getUserData();
        //location.reload();
      } else {
        this.$message({
          message: "请输入正确信息",
          type: "error",
        });
      }
    },

    addFromDetailA() {
      //手动增加助教
      if (
        this.formA.name != "" &&
        this.formA.ta_id != "" &&
        this.formA.email.indexOf("@") >= 0
      ) {
        var jsons = {
          name: this.formA.name,
          ta_id: this.formA.ta_id,
          email: this.formA.email,
          token: sessionStorage.getItem("token"),
        };

        this.axios
          .post("/api/Register/addTAManually", JSON.stringify(jsons))
          .then((response) => {
            this.checkData(response.data);
          });
        this.dialogFormVisibleA = false;
        this.formA.name = "";
        this.formA.ta_id = "";
        this.formA.email = "";
        this.getUserData();
      } else {
        this.$message({
          message: "请输入正确信息",
          type: "error",
        });
      }
      //location.reload();
    },

    addFromExcelS() {
      let fdParams = new FormData();
      this.fileListS.forEach((file) => {
        //console.log(file);
        fdParams.append("file", file.raw);
      });
      //fdParams.append("userID", "123");

      this.axios
        .post("/api/Register/addStudent/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          //timeout: 20000,
        })
        .then((response) => {
          console.log("addFromExcelS", response);
          this.$message.success("添加成功!");
          this.fileListS = [];
          this.getUserData();
          this.dialogExcelVisibleS = false;
        })
        .catch({});
    },

    addFromExcelT() {
      let fdParams = new FormData();
      this.fileListT.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      //fdParams.append("userID", "123");
      console.log("addFromExcelTjson", this.fileListT);
      this.axios
        .post("/api/Register/addTeacher/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          //timeout: 20000,
        })
        .then((response) => {
          console.log("addFromExcelT", response);
          this.$message.success("添加成功!");
          this.fileListT = [];
          this.getUserData();
          this.dialogExcelVisibleT = false;
        })
        .catch({});
    },

    addFromExcelA() {
      let fdParams = new FormData();
      this.fileListA.forEach((file) => {
        console.log(file);
        fdParams.append("file", file.raw);
      });
      //fdParams.append("userID", "123");

      this.axios
        .post("/api/Register/addTA/", fdParams, {
          headers: { "Content-Type": "multipart/form-data" }, //定义内容格式,很重要
          //timeout: 20000,
        })
        .then((response) => {
          console.log(response);
          this.$message.success("添加成功!");
          this.fileListA = [];
          this.getUserData();
          this.dialogExcelVisibleA = false;
        })
        .catch({});
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

    checkData(response) {
      if (response.code == 200) this.$message.success("添加成功");
      else if (response == "UserIDExist") this.$message("学号/工号 已被注册");
      else if (response == "UserMailExist") this.$message("邮箱已被注册");
      else this.$message("网络错误");
      this.getUserData();
    },

    handleCommandDetail(command) {
      if (command == "s") this.handleDetailS();
      else if (command == "t") this.handleDetailT();
      else if (command == "a") this.handleDetailA();
    },

    handleCommandForm(command) {
      if (command == "s") this.handleExcelS();
      else if (command == "t") this.handleExcelT();
      else if (command == "a") this.handleExcelA();
    },
  },
  mounted() {
    this.getUserData();
  },
};
</script>

<style scoped>
.el-dropdown-link {
  cursor: pointer;
  color: #409eff;
}
</style>

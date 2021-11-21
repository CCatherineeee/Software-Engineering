<template>
  <el-card>
    <el-button
      type="info"
      style="background: #7986cb; color: white"
      @click="handleAdd"
      >添加责任教师</el-button
    >
    <el-table
      :data="
        tableData.filter(
          (data) =>
            !search || data.name.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
    >
      <el-table-column label="课程编号" prop="prefix" sortable />
      <el-table-column label="课程名称" prop="name" sortable />
      <el-table-column label="开课学年" prop="year" sortable />
      <el-table-column label="开课学期" prop="semester" sortable />
      <el-table-column label="教师id" prop="t_id" sortable />
      <el-table-column label="教师名称" prop="t_name" sortable />
      <el-table-column align="right">
        <template #header>
          <el-input v-model="search" size="mini" placeholder="Type to search" />
        </template>
        <template #default="scope">
          <el-button size="mini" @click="handleEdit(scope.row)">更改</el-button>
          <el-button size="mini" @click="handleDelete(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="teaDialog" title="添加责任教师" center>
      <el-form ref="form" label-width="80px" style="margin-left: 5%">
        <el-form-item label="课程编号" required>
          <el-select v-model="prefix">
            <el-option
              v-for="item in courseList"
              :key="item.prefix"
              :label="item.title"
              :value="item.prefix"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开课学年" required>
          <el-input v-model="year"></el-input>
        </el-form-item>
        <el-form-item label="开课学期" required>
          <el-select v-model="semester">
            <el-option
              v-for="item in semesterList"
              :key="item"
              :label="item"
              :value="item"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="责任教师" required>
          <el-select v-model="t_id">
            <el-option
              v-for="item in teaList"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="teaDialog = false">取消</el-button>
        <el-button type="primary" @click="addTea()">确定</el-button>
      </div>
    </el-dialog>
  </el-card>
</template>

<script scoped>
import axios from "axios";
export default {
  data() {
    return {
      search: "",

      teaDialog: false,
      courseList: [],

      semesterList: ["Spring", "Autumn"],
      teaList: [],

      prefix: "",
      year: "",
      semester: "",
      t_id: "",
      tableData: [],
    };
  },
  methods: {
    handleEdit(row) {
      this.prefix = row.prefix;
      this.year = row.year;
      this.semester = row.semester;
      this.t_id = row.t_id;
      //this.teaDialog = true;
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    getAllCourse() {
      //获得所有课程
      axios
        .get("/api/course/getType/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => {
          console.log(response);
          this.courseList = response.data;
        })
        .catch(function (error) {
          console(error);
        });
    },
    getAllDutyTea() {
      //已经设置的责任教师
      axios
        .get("/api/course/getDuty/", {
          //params: { userData: "value" },
          crossDomain: true,
        })
        .then((response) => {
          console.log(response);
          this.tableData = response.data;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    handleAdd() {
      this.teaDialog = true;
    },
    addTea() {
      console.log(this.semester);
      var jsons = {
        semester: this.semester,
        year: this.year,
        prefix: this.prefix,
        t_id: this.t_id,
      };
      axios
        .post("/api/course/addDuty/", JSON.stringify(jsons))
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      location.reload();
    },
  },
  mounted() {
    this.getAllCourse();
    this.getAllDutyTea();
  },
};
</script>

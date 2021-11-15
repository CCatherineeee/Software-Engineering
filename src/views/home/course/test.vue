<template>
  <el-form
    ref="experForm"
    style="margin: 40px 100px 0px 50px"
    :model="experForm"
    label-width="80px"
  >
    <el-form-item label="实验名称" prop="name">
      <el-input v-model="experForm.name"></el-input>
    </el-form-item>

    <el-form-item label="实验目的" prop="purpose">
      <el-input v-model="experForm.purpose"></el-input>
    </el-form-item>

    <el-form-item label="实验设备" prop="equipment">
      <el-input v-model="experForm.equipment"></el-input>
    </el-form-item>

    <el-form-item label="实验步骤" prop="step">
      <el-input v-model="experForm.step"></el-input>
    </el-form-item>

    <el-form-item label="实验过程" prop="process">
      <el-input v-model="experForm.process"></el-input>
    </el-form-item>

    <el-form-item label="结果分析" prop="result">
      <el-input v-model="experForm.result"></el-input>
    </el-form-item>

    <el-form-item>
      <el-button style="margin-left: 80px" @click="save()" type="primary"
        >保存修改</el-button
      >
      <el-button style="margin-left: 100px" @click="back">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      experForm: {
        name: "",
        purpose: "",
        equipment: "",
        step: "",
        process: "",
        result: "",
      },
    };
  },
  methods: {
    save() {},
    back() {
      this.$router.push("/teacherHome/concreteCourse/Exper");
    },
  },
};
</script>

<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="所有人" name="first">
      <el-input
        placeholder="请输入学号或姓名"
        v-model="searchP"
        style="width: 20%"
        clearable
      />
      <el-table
        :data="
          tableData.filter(
            (data) =>
              !searchP ||
              data.name.toLowerCase().includes(searchP.toLowerCase()) ||
              data.id.toLowerCase().includes(searchP.toLowerCase()) ||
              data.role.toLowerCase().includes(searchP.toLowerCase())
          )
        "
        style="width: 100%"
      >
        <el-table-column prop="id" label="学号" sortable />
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
      <el-input
        placeholder="请输入学号或姓名"
        v-model="searchG"
        style="width: 20%"
        clearable
      />

      <div v-for="(data, index) in groupData" :key="index">
        <el-card shadow="hover" class="box-card">
          <el-collapse @change="handleChange">
            <el-collapse-item :title="data.leader">
              <div v-for="(data, index) in data.member" :key="index">
                {{ data.name }}
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </div>
      <v-expansion-panels focusable>
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
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
      searcP: "",
      searcG: "",
      tableData: [
        {
          name: "王小虎",
          id: "2016-05-02",
          role: 1,
        },
        {
          id: "2016-05-04",
          name: "王小虎",
          role: 1,
        },
        {
          id: "2016-05-01",
          name: "王小虎",
          role: 2,
        },
        {
          id: "2016-05-03",
          name: "王小虎",
          role: 2,
        },
      ],
      groupData: [
        {
          leader: "组长",
          member: [
            {
              name: "1",
            },
            {
              name: "2",
            },
          ],
        },
        {
          leader: "组长",
          member: [
            {
              name: "1",
            },
            {
              name: "2",
            },
          ],
        },
      ],
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
  },
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
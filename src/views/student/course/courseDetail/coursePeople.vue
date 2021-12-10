<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="所有人" name="first">
      <el-input
        placeholder="请输入学号或姓名"
        :v-model="searchP"
        style="width: 20%"
        clearable
      />
      <el-table
        :data="
          stuList.filter(
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
          <el-collapse>
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
      searchP: "",
      searchG: "",
      class_id: "",
      stuList: [],
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
    getStuList() {
      this.axios
        .post(
          "/api/manageClass/IDGetClassStudent",
          JSON.stringify({
            class_id: this.class_id,
            token: sessionStorage.getItem("token"),
          })
        )
        .then((response) => {
          console.log("getStu");
          console.log(response);

          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.stuList = response.data.data["data"];
          }
        });
    },
    getParams: function () {
      this.id = sessionStorage.getItem("id");
      this.class_id = JSON.parse(this.$Base64.decode(this.$route.query.info))[
        "class_id"
      ];
      console.log("cid===" + this.class_id);
    },
  },
  mounted() {
    this.getParams();
    this.getStuList();
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
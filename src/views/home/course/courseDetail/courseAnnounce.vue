<template>
  <div class="block">
    <el-container>
      <el-main>
        <el-timeline>
          <el-timeline-item
            v-for="(data, index) in dataTable"
            :key="index"
            center
            placement="top"
            :timestamp="data.time"
          >
            <el-card>
              <h2>{{ data.title }}</h2>
              <el-link @click="handleTitle(data)">{{ data.content }}</el-link>
              <p style="text-align: right">{{ data.name }}</p>
            </el-card>
          </el-timeline-item>
        </el-timeline>
        <el-dialog :visible.sync="dialogVisible" :title="this.title" center>
          <span class="dialogBack">{{ this.content }}</span>
          <div slot="footer" class="dialog-footer">
            <el-button type="primary" @click="dialogVisible = false"
              >确定</el-button
            >
          </div>
        </el-dialog>
      </el-main>
      <el-aside></el-aside>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: "",
      content: "",
      dialogVisible: false,
      dataTable: [
        {
          time: "时间1",
          title: "标题1",
          content: "内容1",
          name: "人1",
        },
        {
          time: "2",
          title: "2.1",
          content: "2.2",
          name: "2.3",
        },
        {
          time: "3",
          title: "3.1",
          content: "3.2",
          name: "3.3",
        },
      ],
    };
  },
  methods: {
    handleTitle(data) {
      this.title = data.title;
      this.content = data.content;
      this.dialogVisible = true;
    },
  },
};
</script>
<template>
<el-col :span="12">
    <el-upload
            class="upload-import"
            ref="uploadImport"
            action="https://baidu.com/" 
            :on-remove="handleRemove"
            :on-change="handleChange"
            :file-list="fileList"
            :limit="3" 
            :auto-upload="false"	
            accept="application/vnd.ms-excel,.csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,">  <!-- 设置接收的文件类型--             :on-change="handleChange" -->
            <!-- el-upload组件,在手动上传时,禁用按钮外, 还需要设置    :disabled="hasFile"   为true禁用该组件,会导致上传列表也被禁用,无法删除,因此使用v-show,文件数量为1时,显示禁用的的按钮, slot不绑定trigger事件 --> 
          <el-button  size="small" type="primary">选取文件</el-button>
          <div slot="tip" class="el-upload__tip">只能上传excel文件，且不超过10M</div>
      </el-upload>

          <el-button @click="onSureHandle" type="primary">上传</el-button>
</el-col>

</template>

<script>
 export default {
    data() {
      return {
        fileList: []
      };
    },
    methods: {
      handleRemove(file, fileList) {
        console.log(file);
        console.log(fileList);
      },
      handleChange(file) {
        console.log(file);
        this.fileList.push(file);
        console.log(this.fileList);
      
      },

      onSureHandle(){
	
						let fdParams = new FormData();
            this.fileList.forEach(file => {
              console.log(file)
              fdParams.append('file', file.raw)
            })
            fdParams.append('userID',"123")
						

					this.axios.post('/api/file/addUser/', fdParams, {
							headers: {'Content-Type': 'multipart/form-data'},//定义内容格式,很重要
							timeout: 20000,
						}).then((response) => {
							console.log(response)
						}).catch({})						

      }

      
    }
  }
</script>
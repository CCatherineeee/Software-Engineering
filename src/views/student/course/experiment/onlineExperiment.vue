<template>

      <el-container >
        <el-header>
          <!-- <el-col :span="16" align="left">{{ auction.auctionName }}</el-col>
          <el-col :span="8" align="right" justify="right">{{ isIn ? '未参加' : '已参加' }}</el-col> -->
          <el-col :span="12">
          <h3>您本次实验的角色为：{{role}}。请选择您的竞品和竞价：</h3>
          </el-col>

          <el-col :span="4" align="right" justify="right">
            <el-select v-model="goodType" placeholder="请选择">
              <el-option
                v-for="item in types"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-col>

           <el-col :span="4" align="right" justify="right">
              <el-input-number v-model="myprice"  :min="1" :max="1000" label="请输入您的竞价" ></el-input-number>
          </el-col>

           <el-col :span="4" align="right" justify="right">
              <el-button @click="submitPrice">提交</el-button>
          </el-col>
        </el-header>
            
        <el-container>
          <el-aside style="width:330px">
            <h4 style="text-align:center;margin-top:20px;">意愿竞拍所得表</h4>
            <el-table :data="totalProfitList.slice((currentPage-1)*pagesize,currentPage*pagesize)" border style="width: 100%;margin-top:20px;">
              <el-table-column prop="type" label="品种" width="60px"></el-table-column>
              <el-table-column prop="price" label="价格" width="60px"></el-table-column>
              <el-table-column prop="buyerNum" label="报价者数" width="80px"></el-table-column>
              <el-table-column prop="sellNum" label="出售数" width="70px"></el-table-column>
              <el-table-column prop="profit" label="收益" width="59px"></el-table-column>
            </el-table>
          <div style="text-align: center;margin-top: 30px;">
            <el-pagination
              background
              layout="prev, pager, next"
              :total="total"
              @current-change="current_change">
            </el-pagination>
          </div>
          </el-aside>
          <el-main>
            <el-descriptions title="拍卖情况">
              <el-descriptions-item label="发起人">{{starter}}</el-descriptions-item>
              <el-descriptions-item label="竞价次数">{{times}}</el-descriptions-item>
              <el-descriptions-item label="结束时间">{{stop_time}}</el-descriptions-item>
            </el-descriptions>

            <el-tabs title="tab" v-model="activeName" type="border-card" @tab-click="handleClick">
              <el-tab-pane label="需求-价格关系图" name="first" :key="'first'">
                <div style="background: yellow; display: inline">
                </div>
              </el-tab-pane>

              <el-tab-pane label="供给-价格关系图" name="second" :key="'second'">
                <div style="background: green; display: inline">
                </div>
              </el-tab-pane>

              <el-tab-pane label="供需平衡关系图" name="third" :key="'third'">
                <div style="background: green; display: inline">
                </div>
              </el-tab-pane>
              <div id="myChart" style="width: 420px; height: 360px;"/>
              <!--nodata弹窗-->
              <div v-if="isNoData">
                  No Data
              </div>

            </el-tabs>
          </el-main>
        </el-container>

      </el-container>

</template>


<script>
export default {
  data() {
    return {
      activeName: 'first',
      sid:null,
      ex_id:null,
      role:null,
      myprice:null,
      goodType:1,
      isNoData:false,
      stop_time:null,
      times:null,
      starter:null,
      total: 0,
      pagesize:8,
      currentPage:1,
      types:[{
        value:1,
        label:"茶壶"
      },{
        value:2,
        label:"背包"
      },{
        value:3,
        label:"抱枕"
      }],
      auction: {
        id: 0,
        initiator: '',
        auctionName: 'name',
        startTime: '',
        endTime: '',
        participationNum: 0
      },

      xDemandData:[], //放x轴的范围  （统计茶壶、背包和枕头的最大x值，放进来）
      yDemandPotData:[],  //放y轴茶壶的数据
      yDemandBagData:[],  //放y轴背包的数据
      yDemandPillowData:[], //放y轴枕头的数据
      xProvideData:[],
      yProvidePotData:[],
      yProvideBagData:[],
      yProvidePillowData:[],
      xBalanceData:[],
      totalProfitList:[],

    }
  },
  created() {
    // console.log(this.auction)
    this.getParams();
    this.getDemand();
    this.getProvide();
    this.getAuctionRole();
    this.getProfitList();
    this.getTimes();
    this.getStarter();
    this.drawDemandLine();

  },
  mounted(){
    if(this.xDemandData.length==0)
    {
      this.isNoData=true;
    }
    else 
    {this.drawDemandLine();}
  },
  methods: {
    handleClick(){
      var echarts = require('echarts');
      let myChart = echarts.init(document.getElementById('myChart'));
      myChart.clear();
      //console.log(this.activeName);
      if(this.activeName=="second")
      {
        if(this.xProvideData.length==0)
        {
          this.isNoData=true;
        }
        else {
          this.isNoData = false;
          this.drawProvideLine();
          }
      }
      else if(this.activeName=="first")
      {
        if(this.xDemandData.length==0)
        {
          this.isNoData=true;
        }
        else 
        {
          this.isNoData = false;
          this.drawDemandLine();
          }
      }
      else if(this.activeName=="third"){
        if(this.xProvideData.length==0 || this.xDemandData.length==0)
        {
          this.isNoData=true;
        }
        else{
          if(this.xDemandData.length>this.xProvideData.length)
          {
            this.xBalanceData=this.xDemandData;
          }
          else{
            this.xBalanceData=this.xProvideData;
          }
          this.drawBalanceLine();
          }
      }
    },
      getParams(){
        const routerParams = this.$route.query;
        this.sid = routerParams.sid;
        this.ex_id = routerParams.ex_id;
        this.stop_time = routerParams.stop_time;
        console.log(routerParams);
      },
      submitPrice(){
      var price = this.myprice;
      var jsons = {
        s_id: this.sid,
        token: sessionStorage.getItem("token"),
        ex_id: this.ex_id,
        price: this.myprice,
        good: this.goodType,
        role: this.role
      };
      this.axios
        .post("/api/auction/addAuctionItem", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            var times = response.data["data"]
            this.$message("竞价成功,您第"+times+"次竞价的价格为"+price+"元");
            this.$router.go(0);  //刷新页面
            // this.course_name = response.data.data.course_name;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      },

      getDemand(){
      var jsons = {
        ex_id: this.ex_id,
      };
      this.axios
        .post("/api/auction/getDemand", JSON.stringify(jsons))
        .then((response) => {
          console.log(response);
          if (response.data["code"] === 400) {
            this.$message("找不到该实验");
          }  else {
            var res = response
            this.xDemandData = res.data["data"]["xData"];
            this.yDemandPotData = res.data["data"]["yPotData"];
            this.yDemandBagData = res.data["data"]["yBagData"];
            this.yDemandPillowData = res.data["data"]["yPillowData"]
          
            // this.course_name = response.data.data.course_name;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      getProvide(){
        var jsons = {
        ex_id: this.ex_id,
      };
      this.axios
        .post("/api/auction/getProvide", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 400) {
            this.$message("找不到该实验");
          }  else {
            var res = response
            this.xProvideData = res.data["data"]["xData"];
            this.yProvidePotData = res.data["data"]["yPotData"];
            this.yProvideBagData = res.data["data"]["yBagData"];
            this.yProvidePillowData = res.data["data"]["yPillowData"]
            
            // this.course_name = response.data.data.course_name;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      getBalance(goodType){
        console.log(goodType);
      },
      getAuctionRole(){
        var jsons = {
        s_id: this.sid,
        token: sessionStorage.getItem("token"),
        ex_id: this.ex_id,
      };
      this.axios
        .post("/api/auction/getAuctionRole", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 301) {
            this.$message("验证过期");
            this.$router.push({ path: "/login" });
          } else if (response.data["code"] === 404) {
            this.$message("找不到页面");
            this.$router.push({ path: "/404" });
          } else {
            this.role = response.data["data"];
            // this.course_name = response.data.data.course_name;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      drawDemandLine(){
        var echarts = require('echarts');
        // 基于准备好的dom，初始化echarts实例
        let myChart = echarts.init(document.getElementById('myChart'));
        myChart.clear();
        var option3 = {
            title:{
                text: '需求-价格关系图'
            },
            legend:{
                data:['茶壶','背包','抱枕'],
                x: 'right',
                y: 'top'
            },
            xAxis:{
                data:this.xDemandData
            },
            yAxis:{},
            series:[
                {
                    name:'茶壶',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#c3f" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#c3f"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年apple的数量
                    data: this.yDemandPotData
                },
                {
                    name:'背包',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#3fc" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#3fc"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年banana的数量
                    data: this.yDemandBagData
                },
                {
                    name:'抱枕',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#fcf" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#fcf"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yDemandPillowData
                }
            ]
        };
        myChart.setOption(option3);
        myChart.resize();

        },
        drawProvideLine(){
        var echarts = require('echarts');
        // 基于准备好的dom，初始化echarts实例
        let myChart = echarts.init(document.getElementById('myChart'));
        myChart.clear();
        var option3 = {
            title:{
                text: '供应-价格关系图'
            },
            legend:{
                data:['茶壶','背包','抱枕'],
                x: 'right',
                y: 'top'
            },
            xAxis:{
                data:this.xProvideData
            },
            yAxis:{},
            series:[
                {
                    name:'茶壶',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#c3f" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#c3f"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年apple的数量
                    data: this.yProvidePotData
                },
                {
                    name:'背包',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#3fc" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#3fc"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年banana的数量
                    data: this.yProvideBagData
                },
                {
                    name:'抱枕',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#fcf" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#fcf"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yProvidePillowData
                }
            ]
        };
        myChart.setOption(option3);
        myChart.resize();

        },
      drawBalanceLine(){
        var echarts = require('echarts');
        // 基于准备好的dom，初始化echarts实例
        let myChart = echarts.init(document.getElementById('myChart'));
        myChart.clear();
        var option3 = {
            legend:{
                data:['茶壶需求','背包需求','抱枕需求','茶壶供给','背包供给','抱枕供给'],
                x: 'left',
                y: 'top'
            },
            xAxis:{
                data:this.xBalanceData
            },
            yAxis:{},
            series:[
                {
                    name:'茶壶需求',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#c3f" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#c3f"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年apple的数量
                    data: this.yDemandPotData
                },
                {
                    name:'背包需求',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#3fc" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#3fc"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年banana的数量
                    data: this.yDemandBagData
                },
                {
                    name:'抱枕需求',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#fcf" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#fcf"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yDemandPillowData
                },
                {
                    name:'茶壶供给',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#99CCFF" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#99CCFF"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yProvidePotData
                },
                {
                    name:'背包供给',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#CCCCFF" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#CCCCFF"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yProvideBagData
                },
                {
                    name:'抱枕供给',
                    type:'line',
                    itemStyle:{
                        normal:{ color: "#FFCC99" } //坐标圆点的颜色
                    },
                    lineStyle:{
                        normal:{ width:2,color: "#FFCC99"  }//线条的颜色及宽度
                    },
                    label: {//线条上的数字提示信息
                        normal: {
                            show: true,
                            position: 'top'
                        }
                    },
                    smooth: true,//线条平滑
                    //data为每年egg的数量
                    data: this.yProvidePillowData
                },
            ]
        };
        myChart.setOption(option3);
        myChart.resize();

      },
    getProfitList(){
        var jsons = {
        ex_id: this.ex_id,
      };
      this.totalProfitList= []
      this.axios
        .post("/api/auction/getProfitTable", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 400) {
            this.$message("找不到该实验");
          }  else {
            var data = response.data["data"];
            this.total = data.length;
            for(var i=0;i<data.length;i++)
            {
              var result_json = {
                "type":data[i][0],
                "price":data[i][1],
                "buyerNum":data[i][2],
                "sellNum":data[i][3],
                "profit":data[i][4]
                };
                this.totalProfitList.push(result_json);
            }
        }
      })
        .catch(function (error) {
          console.log(error);
        });
    },
    getTimes(){
        var jsons = {
        ex_id: this.ex_id,
      };

      this.axios
        .post("/api/auction/getExCount", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 400) {
            this.$message("找不到该实验");
          } 
           else {
            var data = response.data["data"];
            this.times = data;
        }
      })
        .catch(function (error) {
          console.log(error);
        });
    },
    getStarter(){
        var jsons = {
        ex_id: this.ex_id,
      };
      this.totalProfitList= []
      this.axios
        .post("/api/auction/getStarter", JSON.stringify(jsons))
        .then((response) => {
          if (response.data["code"] === 400) {
            this.$message("找不到该实验");
          } 
          else if(response.data["code"] === 500){
            this.$message("找不到发起人");
          }
           else {
            var data = response.data["data"];
            this.starter = data;
        }
      })
        .catch(function (error) {
          console.log(error);
        });
    },
    current_change(current){
      this.currentPage=current;
    },
      }
}
</script>


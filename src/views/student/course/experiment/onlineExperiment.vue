<template>

      <el-container >
        <el-header>
          <el-col :span="16" align="left">{{ auction.auctionName }}</el-col>
          <el-col :span="8" align="right" justify="right">{{ isIn ? '未参加' : '已参加' }}</el-col>
        </el-header>
        <el-container>
          <el-aside>
            <el-row align="center"  style="text-aligh:center;">意愿竞拍所得表</el-row>
            <el-table :data="totalProfitList" border style="width: 100%">
              <el-table-column prop="price" label="价格" width="80px"></el-table-column>
              <el-table-column prop="buyerNum" label="报价者数" width="70px"></el-table-column>
              <el-table-column prop="sellNum" label="出售数" width="70px"></el-table-column>
              <el-table-column prop="profit" label="收益" width="79px"></el-table-column>
            </el-table>
          </el-aside>
          <el-main>
            <el-row>
              <el-col :span="8" align="left">发起人： {{ auction.initiator }}</el-col>
              <el-col :span="12" align="left">发起时间： {{ auction.startTime }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="8" align="left">参加人数： {{ auction.participationNum }}</el-col>
              <el-col :span="12" align="left">结束时间： {{ auction.endTime }}</el-col>
            </el-row>
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
              <div id="myChart" style="width: 600px; height: 400px;"/>

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
      isFirst: true,
      isSecond: false,
      isThird: false,
      isShow: false,
      chart: null,
      isDetail: true,
      isIn: false,
      auction: {
        id: 0,
        initiator: '',
        auctionName: 'name',
        startTime: '',
        endTime: '',
        participationNum: 0
      },
      participation: null,
      buyerList: [],
      sellerList: [],
      buyerNumList: [],
      sellerNumList: [],
      totalProfitList: []
    }
  },
  created() {
    // console.log(this.auction)
    window.that = this
    this.getParams()
  },
  methods: {
      getParams(){
        const routerParams = this.$route.query;
        console.log(routerParams);
        if (routerParams!=null){
          // this.addData()
          this.modal=true;
          this.detail.inspector=routerParams;
        }
      },
      }
}
</script>

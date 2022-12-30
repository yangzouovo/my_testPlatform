<template>
  <div class="app-container" id="release130">
    <div style="margin: 6px 0 10px 0;position: relative;">
      <el-row :gutter="20" style="margin-bottom:35px;" type="flex" >
        <el-select v-model="filter_status" style="margin-left: 10px;" placeholder="筛选测试状态" clearable>
          <!-- <el-option label="全部" value= ''></el-option> -->
          <el-option v-for="(value, index) in statusset"  :key="value" :value="index"></el-option>
        </el-select>
        <!-- 时间过滤框 -->
        <!-- <el-date-picker type="daterange" start-placeholder="起始时间" end-placeholder="结束时间"></el-date-picker> -->
        <div style="display:inline-block;position:absolute;right:150px;">   
          <el-tooltip class="item" effect="light" content="仅载入并展示最近1月内的报告数据" placement="left">
            <el-button type="primary" @click="refreshData()">
              重新载入数据
            </el-button>
          </el-tooltip>
        </div>
      </el-row>
    </div>
    <el-table
      v-loading="listLoading"
      :data="filtedData.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index+1 }}
          <!-- <span style="color: #007bff">{{scope.$index+1}}</span> -->
        </template>
      </el-table-column>
      <el-table-column align="center" label="构建编号" width="110" sortable>
        <template slot-scope="scope">
          {{ scope.row.build_number }}
          <!-- <span style="color: #007bff">{{scope.$index+1}}</span> -->
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="本次测试时间" width="300">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.test_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="server编译时间" width="300">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.server_build_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="api版本" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.version }}
        </template>
      </el-table-column>
      <el-table-column label="失败/总用例数" width="150" align="center">
        <template slot-scope="scope">
          {{ scope.row.total_falied }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="测试状态" width="150" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">
            <div v-if="scope.row.status==0"> {{ "全部通过" }} </div> 
            <div v-if="scope.row.status==1"> {{ "需检查" }} </div> 
            <div v-if="scope.row.status==2"> {{ "不通过" }} </div> 
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="goid1" label="详细信息" align="center">
        <template slot-scope="scope">
          <el-button type="primary" @click="getInfoMsg(scope.row.build_number)">点击查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination style="margin: 20px 0px" background @size-change="handleSizeChange"
      @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20, 40]"
      :page-size="pagesize" layout="total, sizes, prev, pager, next, jumper" :total="filtedData.length">
    </el-pagination>
  </div>
</template>

<script>
import { getApiJavaResults,refreshApiJavaResults,getApiJavaInfo } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        0: 'success',
        1: 'warning',
        2: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      filter_testType:'',
      filter_status: null,
      list: [],
      testTypeset:new Set(),
      statusset:{'全部通过':0,
                  '需检查':1,
                  '不通过':2},
      listLoading: true,
      // 分页
      currentPage: 1, //初始页
      pagesize: 10, //    每页的数据
    }
  },
  created() {
    this.fetchData()
  },
  computed: {
    filtedData () {
      return this.list.filter((item) => {
        return this.filter_testType === '' || item.test_type === this.filter_testType
      }).filter((item) => {
        return this.filter_status === null || this.filter_status === '' || item.status === this.statusset[this.filter_status]
      })
    }
  },

  methods: {
    handleSizeChange: function (size) {
      this.pagesize = size;
      // console.log(this.pagesize); //每页下拉显示数据
      // this.pagelist = [];
      // this.fetchPageData(this.currentPage,this.pagesize);
    },
    handleCurrentChange: function (currentPage) {
      this.currentPage = currentPage;
      // console.log(this.currentPage); //点击第几页
      // this.pagelist = [];
      // this.fetchPageData(this.currentPage,this.pagesize);
    },
    fetchData() {
      this.listLoading = true
      getApiJavaResults('release130').then(response => {
        this.list=response.data
        for (var i=0; i<response.data.length; i++){
          // console.log(response.data[i])
          this.testTypeset.add(response.data[i]['test_type'])
        }
        console.log(this.list[0])
        this.listLoading = false
      })
    },
    refreshData() {
      this.listLoading = true
      refreshApiJavaResults().then(response => {
          // console.log(response)
          if(response.code == 20000){
            this.list = []
            this.fetchData()
          } 
      this.listLoading = false
      })
    },
    getInfoMsg(build_number){
      getApiJavaInfo(build_number).then(response =>{
        // let str = response.data
        // let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
        // saveAs(strData, "info.txt");

        const html = response.data
        var newwindow = window.open('', "_blank","toolbar=yes, location=yes, directories=no, status=no, menubar=yes, scrollbars=yes, resizable=no, copyhistory=yes, width=1200, height=800");
        newwindow.document.write(html);
        newwindow.moveTo(500, 200);
        newwindow.document.close()

        // // res.data 为接口返回的html完整文件代码
        // // 必须要存进localstorage，否则会报错，显示不完全
        // window.localStorage.removeItem('callbackHTML')
        // window.localStorage.setItem('callbackHTML', response.data)
        // // 读取本地保存的html数据，使用新窗口打开
        // var newWin = window.open('', '_blank')
        // newWin.document.write(localStorage.getItem('callbackHTML'))
        // // 关闭输出流
        // newWin.document.close()

      })
    },

  }
}
</script>

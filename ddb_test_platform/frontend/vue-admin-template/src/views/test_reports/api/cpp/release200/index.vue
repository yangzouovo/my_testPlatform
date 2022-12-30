<template>
    <div class="app-container" id="release200">
      <div style="margin: 6px 0 10px 0;position: relative;">
        <el-row :gutter="20" style="margin-bottom:35px;" type="flex" >
          <el-select v-model="filter_status" style="margin-left: 20px;" placeholder="筛选测试状态" clearable>
            <el-option label="全部" value= ''></el-option>
            <el-option v-for="(value, index) in statusset"  :key="value" :value="index"></el-option>
          </el-select>
          <!-- 时间过滤框 -->
          <!-- <el-date-picker type="daterange" start-placeholder="起始时间" end-placeholder="结束时间"></el-date-picker> -->
          <div style="display:inline-block;position:absolute;right:58px;">   
            <el-button type="primary" @click="refreshData()">
              重新载入数据
              </el-button>  
          </div>
        </el-row>
      </div>
      <el-table
        v-loading="listLoading"
        :data="filtedData"
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
        <el-table-column label="版本" width="110" align="center">
          <template slot-scope="scope">
            {{ scope.row.version }}
          </template>
        </el-table-column>
        <el-table-column label="失败/总用例数" width="110" align="center">
          <template slot-scope="scope">
            {{ scope.row.total_falied }}
          </template>
        </el-table-column>
        <el-table-column class-name="status-col" label="测试状态" width="110" align="center">
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
            <el-button type="primary" @click="getInfoMsg(scope.row.id)">点击查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </template>
  
  <script>
  import { getApiCppResults,refreshApiCppResults,getApiCppInfo } from '@/api/table'
  
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
        listLoading: true
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
      fetchData() {
        this.listLoading = true
        getApiCppResults().then(response => {
          // this.list = response.data.filter(version => version == 'release200')
          for (var i=0; i<response.data.length; i++){
            // console.log(response.data[i])
            if(response.data[i]['version'] == 'release200'){
              this.list.push(response.data[i])
              this.testTypeset.add(response.data[i]['test_type'])
              // this.statusset.add(response.data[i]['status'])
            }
          }
          console.log(this.list[0])
          this.listLoading = false
        })
      },
      refreshData() {
        this.listLoading = true
        refreshApiCppResults().then(response => {
            // console.log(response)
            if(response.code == 20000){
              this.list = []
              this.fetchData()
            } 
        this.listLoading = false
        })
      },
      getInfoMsg(id){
        getApiCppInfo(id).then(response =>{
          // let str = response.data
          // let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
          // saveAs(strData, "info.txt");
          const text = response.data.replace(/(\n|\r|\r\n|↵)/g, '<br/>')
          var html = '<body><form action="" method="post">'+text+'</form></body>';
          var newwindow = window.open('', "_blank","toolbar=yes, location=yes, directories=no, status=no, menubar=yes, scrollbars=yes, resizable=no, copyhistory=yes, width=1000, height=800");
          newwindow.document.write(html);
          newwindow.moveTo(500, 200);
        newwindow.document.close()
        })
      },
  
    }
  }
  </script>
  
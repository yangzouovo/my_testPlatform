<template>
  <div class="app-container" id="release200">
    <div style="margin: 6px 0 10px 0;position: relative;">
      <el-row :gutter="20" style="margin-bottom:35px;" type="flex">
        <el-select v-model="filter_testType" filterable style="left:10px;" placeholder="筛选测试类型" clearable>
          <!-- <el-option label="全部" value= null></el-option> -->
          <el-option v-for="(value, index) in testTypeset" :key="index" :value="value"></el-option>
        </el-select>
        <el-select v-model="filter_status" filterable style="margin-left: 30px;" placeholder="筛选测试状态" clearable>
          <!-- <el-option label="全部" value= ''></el-option> -->
          <el-option v-for="(value, index) in statusset" :key="value" :value="index"></el-option>
        </el-select>
        <el-select v-model="filter_testTime" filterable style="margin-left: 20px;" placeholder="筛选测试时间" clearable>
          <!-- <el-option label="全部" value= ''></el-option> -->
          <el-option v-for="(value, index) in testTimeset" :key="index" :value="value.substring(0, 10)"></el-option>
        </el-select>
        <el-select v-model="filter_version" filterable style="margin-left: 20px;" placeholder="筛选测试版本" clearable>
          <!-- <el-option label="全部" value= ''></el-option> -->
          <el-option v-for="(value, index) in versionset" :key="index" :value="value"></el-option>
        </el-select>

        <div style="display:inline-block;position:absolute;right:115px;">
          <el-tooltip class="item" effect="light" content="仅载入并展示最近1月内的报告数据" placement="left">
            <el-button type="primary" @click="refreshData()">
              重新载入数据
            </el-button>
          </el-tooltip>
        </div>
      </el-row>
    </div>
    <el-table v-loading="listLoading" :data="filtedData.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
      element-loading-text="Loading" border fit highlight-current-row>
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
          <!-- <span style="color: #007bff">{{scope.$index+1}}</span> -->
        </template>
      </el-table-column>
      <el-table-column label="测试类型" width="250" align="center">
        <template slot-scope="scope">
          {{ scope.row.test_type }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="本次测试时间" width="300">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.test_time }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="plugin编译时间" width="300">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.plugin_build_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="版本" width="160" align="center">
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
            <div v-if="scope.row.status == 0"> {{ "全部通过" }} </div>
            <div v-if="scope.row.status == 1"> {{ "需检查" }} </div>
            <div v-if="scope.row.status == 2"> {{ "不通过" }} </div>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="goid1" label="详细信息" align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-search" @click="getInfoMsg(scope.row.id)">点击查看</el-button>
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
import { getPluginResults, refreshPluginResults, getPluginInfo } from '@/api/table'

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
      filter_testType: '',
      filter_status: null,
      filter_testTime: '',
      filter_version: '',
      list: [],
      // pagelist:[],
      testTypeset: new Set(),
      testTimeset: new Set(),
      versionset: new Set(),
      statusset: {
        '全部通过': 0,
        '需检查': 1,
        '不通过': 2
      },
      listLoading: true,
      // 分页
      currentPage: 1, //初始页
      pagesize: 10, //    每页的数据
    }
  },
  created() {
    this.fetchAllData();
    // this.fetchPageData(this.currentPage,this.pagesize);
  },
  computed: {
    filtedData() {
      return this.list.filter((item) => {
        return this.filter_testType === '' || item.test_type === this.filter_testType
      }).filter((item) => {
        return this.filter_status === null || this.filter_status === '' || item.status === this.statusset[this.filter_status]
      }).filter((item) => {
        return this.filter_testTime === '' || item.test_time.includes(this.filter_testTime)
      }).filter((item) => {
        return this.filter_version === '' || item.version.includes(this.filter_version)
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
    fetchAllData() {
      this.listLoading = true
      getPluginResults(0, null, 'release200', null).then(response => {
        this.list = response.data
        this.testTypeset = response.types
        this.testTimeset = response.times
        this.versionset = response.versions
        // console.log(this.list[0])
        this.listLoading = false
      })
    },
    // fetchPageData(page, pagesize) {
    //   this.listLoading = true
    //   getPluginResults(1, page, 'release200',pagesize).then(response => {
    //     this.pagelist = response.data
    //     // console.log(this.list[0])
    //     this.listLoading = false
    //   })
    // },
    refreshData() {
      this.listLoading = true
      refreshPluginResults().then(response => {
        // console.log(response)
        if (response.code == 20000) {
          this.list = []
          this.fetchAllData()
        }
        this.listLoading = false
      })
    },
    getInfoMsg(id) {
      getPluginInfo(id).then(response => {
        // let str = response.data
        // let strData = new Blob([str], { type: 'text/plain;charset=utf-8' });
        // saveAs(strData, "info.txt");
        const text = response.data.replace(/(\n|\r|\r\n|↵)/g, '<br/>')
        var html = '<body><form action="" method="post">' + text + '</form></body>';
        var newwindow = window.open('', "_blank", "toolbar=yes, location=yes, directories=no, status=no, menubar=yes, scrollbars=yes, resizable=no, copyhistory=yes, width=1000, height=800");
        newwindow.document.write(html);
        newwindow.moveTo(500, 200);
        newwindow.document.close()
      })
    },

  }
}
</script>

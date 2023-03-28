from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from standard.page_std import GoodsPagination
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template

from parser.report_parser import ApiCppParser, ApiJavaParser, PluginParser, ServerParser, ApiJsParser
from app_report.models import ApiCppTable, ApiJavaTable, PluginTalbe, ServerTalbe,ApiJsTable
from app_report.serializer import ApiCppTableSerializer, ApiJavaTableSerializer, PluginTalbeSerializer, ServerTalbeSerializer,ApiJsTableSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework import filters as rest_filter

from backend.settings import BASE_DIR

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

import datetime

class ApiCppTableViewSet(viewsets.ModelViewSet):
    queryset = ApiCppTable.objects.all()
    serializer_class = ApiCppTableSerializer
    pagination_class = GoodsPagination

    filter_backends = [SearchFilter, OrderingFilter]
    # 过滤字段 通过过滤出的字段来查询
    search_fields = ['ssl_version', 'version', 'status']
    # 排序字段
    ordering_fields = ['build_number']

    def list(self, request, *args, **kwargs):
        ssl_v = request.GET.get('sv')
        api_v = request.GET.get('av')
        queryset = self.get_queryset().filter(ssl_version__contains=ssl_v,
                                              version__contains=api_v).order_by('-test_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ApiCppTableSerializer(instance=page, many=True)
            # return self.get_paginated_response(serializer.data)
            count = self.get_paginated_response(serializer.data).data['count']
            return Response(data={'code': 20000, 'message': '查询成功', 'count': count, "data": serializer.data})

        serializer = ApiCppTableSerializer(instance=queryset, many=True)
        return Response(data={'code': 20000, 'message': '查询成功', "data": serializer.data})

    def getInfo(self, request, *args, **kwargs):
        build_number = int(request.GET.get('build_number')) if request.GET.get(
            'build_number') is not None else -1
        if build_number != -1:
            template = get_template(
                f'{str(BASE_DIR)}/dist/reports/cpp/{build_number}.html')
            return Response(data={'code': 20000, 'message': '查询成功', "data": template.render()})
        else:
            return Response(data={'code': 40001, 'message': '未查询到相关信息', "data": None})


class ApiJavaTableViewSet(viewsets.ModelViewSet):
    queryset = ApiJavaTable.objects.all()
    serializer_class = ApiJavaTableSerializer

    # filter_backends = [SearchFilter,OrderingFilter]
    # # 过滤字段 通过过滤出的字段来查询
    # search_fields = ['test_type','version','status']
    # # 排序字段
    # ordering_fields = ['status']

    def list(self, request, *args, **kwargs):
        api_v = request.GET.get('av')
        queryset = self.get_queryset().filter(version__contains=api_v).order_by('-test_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ApiJavaTableSerializer(instance=page, many=True)
            # return self.get_paginated_response(serializer.data)
            count = self.get_paginated_response(serializer.data).data['count']
            return Response(data={'code': 20000, 'message': '查询成功', 'count': count, "data": serializer.data})

        serializer = ApiJavaTableSerializer(instance=queryset, many=True)
        return Response(data={'code': 20000, 'message': '查询成功', "data": serializer.data})

    def getInfo(self, request, *args, **kwargs):

        build_number = int(request.GET.get('build_number')) if request.GET.get(
            'build_number') is not None else -1
        if build_number != -1:
            template = get_template(
                f'{str(BASE_DIR)}/dist/reports/java/test_result_{build_number}.html')
            return Response(data={'code': 20000, 'message': '查询成功', "data": template.render()})
        else:
            return Response(data={'code': 40001, 'message': '未查询到相关信息', "data": None})


class PluginTalbeViewSet(viewsets.ModelViewSet):
    queryset = PluginTalbe.objects.all()
    serializer_class = PluginTalbeSerializer
    pagination_class = GoodsPagination

    filter_backends = [SearchFilter, OrderingFilter]
    # 过滤字段 通过过滤出的字段来查询
    search_fields = ['test_type', 'version', 'status', 'test_time']
    # 排序字段
    ordering_fields = ['test_time']

    def list(self, request, *args, **kwargs):
        # print(request.GET.get('id'))
        v = request.GET.get('v')
        paginate_flag = request.GET.get('pflag')
        queryset = self.get_queryset().filter(version__contains=v).order_by('-test_time')
        page = None
        if paginate_flag == '1':
            page = self.paginate_queryset(queryset)
        test_type_list = []
        test_time_list = []
        version_list = []
        for val in queryset:
            test_type_list.append(val.test_type)
            test_time_list.append(val.test_time)
            version_list.append(val.version)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            count = self.get_paginated_response(serializer.data).data['count']
            return Response(data={'code': 20000, 'message': '查询成功', 'count': count, "data": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'code': 20000, 'message': '查询成功', 'count': len(queryset), 'types': set(test_type_list), 'times': set(test_time_list), 'versions': set(version_list), "data": serializer.data})

    def getInfo(self, request, *args, **kwargs):
        # print(request.GET.get('id'))
        id = int(request.GET.get('id')) if request.GET.get(
            'id') is not None else -1
        if id != -1:
            datas = PluginTalbe.objects.filter(id=id)
            if len(datas) > 0:
                for data in datas:
                    # print(data.info)
                    # print(data)
                    return Response(data={'code': 20000, 'message': '查询成功', "data": data.info})
            else:
                return Response(data={'code': 20001, 'message': '查询成功', "data": None})
        else:
            return Response(data={'code': 40001, 'message': '未查询到相关信息', "data": None})


class ServerTalbeViewSet(viewsets.ModelViewSet):
    queryset = ServerTalbe.objects.all()
    serializer_class = ServerTalbeSerializer

    # filter_backends = [SearchFilter,OrderingFilter]
    # # 过滤字段 通过过滤出的字段来查询
    # search_fields = ['test_type','version','status']
    # # 排序字段
    # ordering_fields = ['status']

    def list(self, request, *args, **kwargs):
        # print(request.GET.get('id'))
        v = request.GET.get('v')
        paginate_flag = request.GET.get('pflag')
        queryset = self.get_queryset().filter(version__contains=v).order_by('-test_time')
        page = None
        if paginate_flag == '1':
            page = self.paginate_queryset(queryset)
        test_type_list = []
        test_time_list = []
        version_list = []
        for val in queryset:
            test_type_list.append(val.test_type)
            test_time_list.append(val.test_time)
            version_list.append(val.version)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            count = self.get_paginated_response(serializer.data).data['count']
            return Response(data={'code': 20000, 'message': '查询成功', 'count': count, "data": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={'code': 20000, 'message': '查询成功', 'count': len(queryset), 'types': set(test_type_list), 'times': set(test_time_list), 'versions': set(version_list), "data": serializer.data})

    def getInfo(self, request, *args, **kwargs):
        # print(request.GET.get('id'))
        id = int(request.GET.get('id')) if request.GET.get(
            'id') is not None else -1
        if id != -1:
            datas = ServerTalbe.objects.filter(id=id)
            if len(datas) > 0:
                for data in datas:
                    # print(data.info)
                    # print(data)
                    return Response(data={'code': 20000, 'message': '查询成功', "data": data.info})
            else:
                return Response(data={'code': 20000, 'message': '查询成功', "data": None})
        else:
            return Response(data={'code': 40001, 'message': '未查询到相关信息', "data": None})

class ApiJsTableViewSet(viewsets.ModelViewSet):
    queryset = ApiJsTable.objects.all()
    serializer_class = ApiJsTableSerializer

    # filter_backends = [SearchFilter,OrderingFilter]
    # # 过滤字段 通过过滤出的字段来查询
    # search_fields = ['test_type','version','status']
    # # 排序字段
    # ordering_fields = ['status']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-test_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ApiJsTableSerializer(instance=page, many=True)
            # return self.get_paginated_response(serializer.data)
            count = self.get_paginated_response(serializer.data).data['count']
            return Response(data={'code': 20000, 'message': '查询成功', 'count': count, "data": serializer.data})

        serializer = ApiJsTableSerializer(instance=queryset, many=True)
        return Response(data={'code': 20000, 'message': '查询成功', "data": serializer.data})

    def getInfo(self, request, *args, **kwargs):
        build_number = int(request.GET.get('build_number')) if request.GET.get(
            'build_number') is not None else -1
        if build_number != -1:
            template = get_template(
                f'{str(BASE_DIR)}/dist/reports/js/result_{build_number}.html')
            return Response(data={'code': 20000, 'message': '查询成功', "data": template.render()})
        else:
            return Response(data={'code': 40001, 'message': '未查询到相关信息', "data": None})



def apicpp_loadDataToSqlite3():
    parserNew = ApiCppParser('192.168.100.27', 22, 'yzou', 'DolphinDB123')
    parserNew.parseData("/hdd/hdd5/hzy/test_report/api/cpp", "html")

    datas = parserNew.getData()
    # ApiCppTable.objects.all().delete()
    for i in range(len(datas)):
        test_time_ = datas[i]['test_time']
        server_build_time_ = datas[i]['server_build_time']
        build_number_ = datas[i]['build_number']
        version_ = datas[i]['version']
        ssl_version_ = datas[i]['ssl_version']
        total_falied_ = datas[i]['total_falied']
        status_ = datas[i]['status']

        if not ApiCppTable.objects.filter(test_time=test_time_):
            ApiCppTable(test_time=test_time_, server_build_time=server_build_time_,
                        build_number=build_number_, version=version_, ssl_version=ssl_version_, total_falied=total_falied_, status=status_).save()


def apijava_loadDataToSqlite3():
    parserNew = ApiJavaParser('192.168.100.27', 22, 'yzou', 'DolphinDB123')
    parserNew.parseData("/hdd/hdd5/hzy/test_report/api/java", "html")

    datas = parserNew.getData()
    ApiJavaTable.objects.all().delete()
    for i in range(len(datas)):
        test_time_ = datas[i]['test_time']
        server_build_time_ = datas[i]['server_build_time']
        build_number_ = datas[i]['build_number']
        version_ = datas[i]['version']
        total_falied_ = datas[i]['total_falied']
        status_ = datas[i]['status']
        if not ApiJavaTable.objects.filter(build_number=build_number_):
            ApiJavaTable(test_time=test_time_, server_build_time=server_build_time_,
                         build_number=build_number_, version=version_, total_falied=total_falied_, status=status_).save()


def plugin_loadDataToSqlite3():
    parserNew = PluginParser('192.168.100.27', 22, 'yzou', 'DolphinDB123')
    parserNew.parseData("/hdd/hdd5/hzy/test_report/plugin/", "txt")

    datas = parserNew.getData()
    infos = parserNew.getInfo()

    for i in range(len(datas)):
        test_type_ = datas[i]['test_type']
        test_time_ = datas[i]['test_time']
        plugin_build_time_ = datas[i]['plugin_build_time']
        version_ = datas[i]['version']
        total_falied_ = datas[i]['total_falied']
        status_ = datas[i]['status']
        info_ = infos[i]
        if not PluginTalbe.objects.filter(test_type=test_type_, test_time=test_time_):
            PluginTalbe(test_type=test_type_, test_time=test_time_, plugin_build_time=plugin_build_time_,
                        version=version_, total_falied=total_falied_, status=status_, info=info_).save()


def server_loadDataToSqlite3():
    parserNew = ServerParser('192.168.100.27', 22, 'yzou', 'DolphinDB123')
    parserNew.parseData("/hdd/hdd5/hzy/test_report/server/", "txt")

    datas = parserNew.getData()
    infos = parserNew.getInfo()
    ServerTalbe.objects.all().delete()
    for i in range(len(datas)):
        test_type_ = datas[i]['test_type']
        test_time_ = datas[i]['test_time']
        server_build_time_ = datas[i]['server_build_time']
        version_ = datas[i]['version']
        total_falied_ = datas[i]['total_falied']
        status_ = datas[i]['status']
        info_ = infos[i]
        # insertRow = ServerTalbe(test_type=test_type_,test_time=test_time_,server_build_time=server_build_time_,version=version_,total_falied=total_falied_,status=status_,info=info_)
        # insertRow.save()
        # if not ServerTalbe.objects.filter(test_type=test_type_, test_time=test_time_):
        ServerTalbe.objects.create(test_type=test_type_, test_time=test_time_, server_build_time=server_build_time_,
                                   version=version_, total_falied=total_falied_, status=status_, info=info_)

def apijs_loadDataToSqlite3():
    parserNew = ApiJsParser('192.168.100.27', 22, 'yzou', 'DolphinDB123')
    parserNew.parseData("/hdd/hdd5/hzy/test_report/api/javascript", "html")

    datas = parserNew.getData()
    ApiJsTable.objects.all().delete()
    for i in range(len(datas)):
        test_time_ = datas[i]['test_time']
        server_build_time_ = datas[i]['server_build_time']
        build_number_ = datas[i]['build_number']
        version_ = datas[i]['version']
        total_falied_ = datas[i]['total_falied']
        status_ = datas[i]['status']
        if not ApiJsTable.objects.filter(build_number=build_number_):
            ApiJsTable(test_time=test_time_, server_build_time=server_build_time_,
                         build_number=build_number_, version=version_, total_falied=total_falied_, status=status_).save()


# 开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # 设置定时任务，选择方式为interval，时间间隔为10s
    # @register_job(scheduler, "interval", seconds=10)
    # 每天固定时间执行任务，对应代码为：
    @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='15', minute='45', second='30', id='task_time', replace_existing=True)
    def my_job():
        print("现在是北京时间 "+str(datetime.datetime.now()),"定时任务启动...")
        apicpp_loadDataToSqlite3()
        apijava_loadDataToSqlite3()
        server_loadDataToSqlite3()
        plugin_loadDataToSqlite3()
        apijs_loadDataToSqlite3()
        print("数据加载完成")
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print("定时任务出错：" + str(e))
    # 有错误就停止定时器
    scheduler.shutdown()

from ast import arg
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from books.models import Books
from books.serializer import BooksSerializer
from rest_framework import filters as rest_filter
import dolphindb

from rest_framework.filters import SearchFilter,OrderingFilter

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = (
        rest_filter.SearchFilter,
        rest_filter.OrderingFilter)

class BooksViewSet(BaseViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    

    filter_backends = [SearchFilter,OrderingFilter]
    # 过滤字段 通过过滤出的字段来查询
    search_fields = ['name','author','id']
    # 排序字段
    ordering_fields = ['id']

    # def get_queryset(self):
    #     queryset = super(BooksViewSet, self).get_queryset()
    #     name = self.request.query_params.get('name')
    #     if name:
    #         queryset = queryset.filter(name__contains=name)
    #     return queryset

    def create(self, request, *args, **kwargs):
        name = request.GET.get('name')
        author = request.GET.get('author')
        serializer = BooksSerializer(data={
            "name":request.GET.get('name'),
            "author":request.GET.get('author')
            })
        ids = Books.objects.filter(name=name,author=author)
        print(ids)
        res = serializer.is_valid(raise_exception=False)
        if res:
            if len(ids) == 0:
                self.perform_create(serializer)
                return Response(data={'code': 20000,'message': '创建成功',"data":serializer.data})
            else:
                return Response(data={'code': 40002,'message':"error:数据重复"})
        else:
            return Response(data={'code': 40000,'message':serializer.errors})

    def list(self, request, *args, **kwargs):
        # print(request.GET.get('name'))
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BooksSerializer(instance=page,many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BooksSerializer(instance=queryset, many=True)
        return Response(data={'code': 20000,'message': '查询成功',"data":serializer.data})

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        users = Books.objects.get(pk=pk)
        ser = BooksSerializer(instance=users,many=False)
        return Response(ser.data)

    def update(self, request, *args, **kwargs):
        ori_name = request.GET.get('origin_name')
        name = request.GET.get('name')
        author = request.GET.get('author')
        ids = Books.objects.filter(name=ori_name)
        print(ids)
        if len(ids) !=0:
            for id in ids:
                self.kwargs['pk']=id.pk
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                data = {'name':name,'author':author}
                serializer = BooksSerializer(instance=instance, data=data, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
                return Response(data={'code': 20000, 'message': '更新成功', "data": serializer.data})
        else:
            return Response(data={'code': 40003,'message': 'error:未找到该数据'})

    def destroy(self, request, *args, **kwargs):
        name = request.GET.get('name')
        author = request.GET.get('author') 
        ids = Books.objects.filter(name=name,author=author)
        # print(ids.all())
        for id in ids:
            print(id.pk)
            self.kwargs['pk'] = id.pk
            instance = self.get_object()
            self.perform_destroy(instance)
        return Response(data={'code': 20000, 'message': '删除成功'})

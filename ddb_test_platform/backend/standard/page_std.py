from rest_framework.pagination import PageNumberPagination

class GoodsPagination(PageNumberPagination):
    page_size = 10 # 每页默认显示条数
    page_size_query_param = 'page_size' # 每页显示条数传参字符串
    page_query_param = 'p' # 显示第几页数据传参
    max_page_size = 100 # 最大页码
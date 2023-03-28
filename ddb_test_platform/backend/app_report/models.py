from django.db import models
from standard.model_std import STATUS_ITEMS
# Create your models here.


class ApiCppTable(models.Model):

    test_time = models.CharField(max_length=30,verbose_name='测试时间', blank=True, null=True)
    server_build_time = models.CharField(max_length=30,verbose_name='server编译时间', blank=True, null=True)
    build_number = models.CharField(max_length=30,verbose_name='jenkins构建序号', blank=True, null=True)
    version = models.CharField(max_length=30,verbose_name='api_cpp版本', blank=True, null=True)
    ssl_version = models.CharField(max_length=30,verbose_name='openssl版本', blank=True, null=True)
    total_falied = models.CharField(max_length=30,verbose_name='总用例数/失败用例数', blank=True, null=True)
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态', blank=True, null=True)

    # django web
    class Meta:
        verbose_name='api_cpp test summary'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'ApiCpp'        # 数据库表的名字
    def __str__(self):
        return self.version    # test version

class ApiJavaTable(models.Model):
    test_time = models.CharField(max_length=30,verbose_name='测试时间', blank=True, null=True)
    server_build_time = models.CharField(max_length=30,verbose_name='server编译时间', blank=True, null=True)
    build_number = models.CharField(max_length=30,verbose_name='jenkins构建序号', blank=True, null=True)
    version = models.CharField(max_length=30,verbose_name='api_java版本', blank=True, null=True)
    total_falied = models.CharField(max_length=30,verbose_name='总用例数/失败用例数', blank=True, null=True)
    status = models.IntegerField(verbose_name='状态', blank=True, null=True)

    # django web
    class Meta:
        verbose_name='api_java test summary'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'ApiJava'        # 数据库表的名字
    def __str__(self):
        return self.version    # test version

class PluginTalbe(models.Model):
    test_type = models.CharField(max_length=100,verbose_name='测试类型', blank=True, null=True)
    test_time = models.CharField(max_length=30,verbose_name='测试时间', blank=True, null=True)
    plugin_build_time = models.CharField(max_length=30,verbose_name='plugin编译时间', blank=True, null=True)
    version = models.CharField(max_length=30,verbose_name='plugin版本', blank=True, null=True)
    total_falied = models.CharField(max_length=30,verbose_name='总用例数/失败用例数', blank=True, null=True)
    status = models.IntegerField(choices=STATUS_ITEMS, verbose_name='状态', blank=True, null=True)
    info = models.CharField(max_length=102400,verbose_name='其他信息', blank=True, null=True)
    # django web
    class Meta:
        verbose_name='plugin test summary'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'Plugin'        # 数据库表的名字
    def __str__(self):            
        return self.version    # test version

class ServerTalbe(models.Model):
    test_type = models.CharField(max_length=100,verbose_name='测试类型', blank=True, null=True)
    test_time = models.CharField(max_length=30,verbose_name='测试时间', blank=True, null=True)
    server_build_time = models.CharField(max_length=30,verbose_name='server编译时间', blank=True, null=True)
    version = models.CharField(max_length=30,verbose_name='server版本', blank=True, null=True)
    total_falied = models.CharField(max_length=30,verbose_name='总用例数/失败用例数', blank=True, null=True)
    status = models.IntegerField(verbose_name='状态', blank=True, null=True)
    info = models.CharField(max_length=102400,verbose_name='其他信息', blank=True, null=True)

    # django web
    class Meta:
        verbose_name='server test summary'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'Server'        # 数据库表的名字
    def __str__(self):            
        return self.version    # test version

class ApiJsTable(models.Model):
    test_time = models.CharField(max_length=30,verbose_name='测试时间', blank=True, null=True)
    server_build_time = models.CharField(max_length=30,verbose_name='server编译时间', blank=True, null=True)
    build_number = models.CharField(max_length=30,verbose_name='jenkins构建序号', blank=True, null=True)
    version = models.CharField(max_length=30,verbose_name='api_js版本', blank=True, null=True)
    total_falied = models.CharField(max_length=30,verbose_name='总用例数/失败用例数', blank=True, null=True)
    status = models.IntegerField(verbose_name='状态', blank=True, null=True)

    # django web
    class Meta:
        verbose_name='api_js test summary'
        verbose_name_plural=verbose_name    # 复数形式
        db_table = 'ApiJs'        # 数据库表的名字
    def __str__(self):
        return self.version    # test version

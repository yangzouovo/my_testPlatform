from django.contrib import admin
from app_report.models import ApiCppTable,ApiJavaTable,PluginTalbe,ServerTalbe   #导入模型类

# Register your models here.

class ApiCppAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_time', 'server_build_time', 'build_number', 'version', 'ssl_version', 'total_falied',
        'status')
    list_filter = ('build_number', 'status','version', 'ssl_version')
    search_fields = ('build_number', 'version', 'ssl_version')
    fieldsets = (
        (None, {
         'fields': (
            ('server_build_time', 'test_time'),
            ('build_number', 'version', 'ssl_version'),
            'status',
            )
        }),
    )
admin.site.register(ApiCppTable, ApiCppAdmin)
admin.site.register(ApiJavaTable)
admin.site.register(PluginTalbe)
admin.site.register(ServerTalbe)


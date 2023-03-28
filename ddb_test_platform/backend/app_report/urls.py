from django.urls import path
from app_report import views
from django.urls import re_path


urlpatterns = [
    # path('', include(router.urls)),
    path('cpp/list/', views.ApiCppTableViewSet.as_view({'get':'list'})),
    # path('cpp/list/refresh/', views.ApiCppTableViewSet.as_view({'get':'loadDataToSqlite3'})),
    path('cpp/list/getinfo', views.ApiCppTableViewSet.as_view({'get':'getInfo'})),

    path('java/list/', views.ApiJavaTableViewSet.as_view({'get':'list'})),
    # path('java/list/refresh/', views.ApiJavaTableViewSet.as_view({'get':'loadDataToSqlite3'})),
    path('java/list/getinfo', views.ApiJavaTableViewSet.as_view({'get':'getInfo'})),

    path('plugin/list/', views.PluginTalbeViewSet.as_view({'get':'list'})),
    # path('plugin/list/refresh/', views.PluginTalbeViewSet.as_view({'get':'loadDataToSqlite3'})),
    path('plugin/list/getinfo', views.PluginTalbeViewSet.as_view({'get':'getInfo'})),

    path('server/list/', views.ServerTalbeViewSet.as_view({'get':'list'})),
    # path('server/list/refresh/', views.ServerTalbeViewSet.as_view({'get':'loadDataToSqlite3'})),
    path('server/list/getinfo', views.ServerTalbeViewSet.as_view({'get':'getInfo'})),

    path('js/list/', views.ApiJsTableViewSet.as_view({'get':'list'})),
    # path('js/list/refresh/', views.ApiJavaTableViewSet.as_view({'get':'loadDataToSqlite3'})),
    path('js/list/getinfo', views.ApiJsTableViewSet.as_view({'get':'getInfo'})),

]
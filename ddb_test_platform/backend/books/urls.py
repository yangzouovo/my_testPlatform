from django.urls import path, include
# from rest_framework import routers   #导入routers
from books import views


# router = routers.DefaultRouter()
# router.register('books', views.BooksViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('', views.BooksViewSet.as_view({'get':'list'})),
    path('insert/', views.BooksViewSet.as_view({'post':'create'})),
    path('update/', views.BooksViewSet.as_view({'post':'update'})),
    path('delete/', views.BooksViewSet.as_view({'post':'destroy'})),
]
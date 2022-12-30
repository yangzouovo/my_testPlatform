from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MyTokenObtainPairView, UserProfileViewSet


router = DefaultRouter()

router.register(r'user/info', UserProfileViewSet, basename='retrieve'),
router.register(r'user/list', UserProfileViewSet, basename='list'),
router.register(r'user/add', UserProfileViewSet, basename='create'),
router.register(r'user/update', UserProfileViewSet, basename='update'),
router.register(r'user/del', UserProfileViewSet, basename='destroy')


urlpatterns = [
    path('', include(router.urls)),
    # path('user/info', UserProfileViewSet.as_view({'get':'retrieve'})),
    # path('user/list', UserProfileViewSet.as_view({'get':'list'})),
    # path('user/add', UserProfileViewSet.as_view({'post':'create'})),
    # path('user/update', UserProfileViewSet.as_view({'post':'update'})),
    # path('user/del', UserProfileViewSet.as_view({'post':'destroy'})),
    # path('user/login', Loginview.as_view()),
    path('user/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('user/login', UserProfileViewSet.as_view({'post':'log_in'})),
    path('user/logout', UserProfileViewSet.as_view({'post':'log_out'})),
]


if __name__ == '__main__':
    pass
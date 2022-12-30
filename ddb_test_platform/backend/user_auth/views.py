from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer
from rest_framework import viewsets
from .models import UserProfile
from .serializer import UserProfileSerializer
from rest_framework import filters as rest_filter
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate, logout

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = (
        rest_filter.SearchFilter,
        rest_filter.OrderingFilter)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserProfileViewSet(BaseViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('id')
    # for i in queryset:
    #     print(i.id,i.user.get_username(),i.avatar,i.role,i.user_id) 
        
    def list(self, request, *args, **kwargs):
        user = request.GET.get("username")
        serializer = None
        if user:
            for i in queryset:
                if i.user.get_username() == user:
                    serializer = self.get_serializer(i)
                    break
                else:
                    pass

            if serializer is not None:
                return Response(data={'code': 20000,'message': '查询成功',"data":serializer.data})
            else:
                return Response(data={'code': 40003,'message': 'not found',"data":None})

        else:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(data={'code': 20000,'message': '查询成功',"data":serializer.data})

    def log_out(self, request, *args, **kwargs):
        logout(request=request)
        res = Response(data={'code': 20000,'message': '成功',"data":None})
        res.delete_cookie('username')
        return res


# class Loginview(APIView):
#     def post(self,request):
#         # user=request.data.get('user') #接收前端提交的用户名
#         username=request.data.get('username')    #获取用户前端传过来的登录账号
#         password=request.data.get('password') #接收前端提交的密码
        #多登录方式一
        # #判断登录账号是用户名还是手机号
        # rule=r'^1[3-9][0-9]{9}$'
        # if not re.findall(rule,username):
        #     #说明输入的是用户名
        #     user_info=User.objects.filter(user=username).first()
        # else:
        #     user_info=User.objects.filter(mobile=username).first()
        #多登录方式二
        # from django.db.models import Q
        # user_info=UserProfile.objects.filter(user=username)
        # print(user_info)
        #判断用户是否存在
        #获取符合条件的第一条数据，如果没有符合条件的，返回的是None
        # user_info=User.objects.filter(user=user).first()
        # if not user_info: #如果用户不存在
        #     return Response({
        #         'code':40003,
        #         'msg':'用户名或密码错误'
        #     })
        # # 程序走到这里，代表用户存在
        # #判断密码对不对
        # if user_info.password!=password: #密码不一致
        #     return Response({
        #         'code': 40004,
        #         'msg': '用户名或密码错误'
        #     })
        # # 程序走到这一步，就代表用户存在且密码输入正确
        # #生成jwt
        # # pip install pyjwt 安装jwt
        # import jwt,time     #导包
        # from django.conf import settings
        # payload={
        #     'user_id':user_info.id, #用户id
        #     'user':user_info.user, #用户名
        #     'exp':int(time.time())+(60*60*24*30)  #起始时间，到什么时候超时 时间戳 这里设置有效期一个月
        # }
        # # payload 载荷
        # # key 私钥
        # # settings.SECRET_KEY   django项目随机生成的一个私钥
        # # algorithm 加密方式
        # token=jwt.encode(payload,key=settings.SECRET_KEY,algorithm='HS256')
        # #程序走到这一步，就一定代表用户存在且密码也输入正确、
        # return Response({
        #     'code':20000,
        #     'msg':'登陆成功',
        #     'user':{ #返回用户信息
        #         'name':user_info.user,
        #         'mobile':user_info.mobile
        #         #密码不能往前台传
        #     },
        #     'token':token
        # })
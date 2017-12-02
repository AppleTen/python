from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'), # 用户注册
    url(r'^register_handle/$', views.register_handle, name='register'), # 用户注册处理
    url(r'^active/(?P<token>.*)/$', views.register_active, name='active'), # 用户激活
    url(r'^login/$', views.login, name='login'), # 用户登录

    url(r'^check_user_exist/$', views.check_user_exist, name='check_user_exist'), # 校验用户名是否存在
]

from django.urls import path, re_path, include
from apps.user.views import RegisterView, ActiveView, LoginView

app_name = 'user'
urlpatterns = [
    # path('register', views.register, name='register'),  # 注册
    # path('register_handle', views.register_handle, name='register_handle'),  # 注册处理
    path('register', RegisterView.as_view(), name='register'),
    path('active/<str:token>', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login'),
]
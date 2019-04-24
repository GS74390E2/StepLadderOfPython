from django.urls import path, re_path, include
from apps.user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView
# from django.contrib.auth.decorators import login_required

app_name = 'user'
urlpatterns = [
    # path('register', views.register, name='register'),  # 注册
    # path('register_handle', views.register_handle, name='register_handle'),  # 注册处理
    path('register', RegisterView.as_view(), name='register'),
    path('active/<str:token>', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    # path('', login_required(UserInfoView.as_view()), name='user'),
    # path('order', login_required(UserOrderView.as_view()), name='order'),
    # path('address', login_required(AddressView.as_view()), name='address'),
    path('', UserInfoView.as_view(), name='user'),
    path('order', UserOrderView.as_view(), name='order'),
    path('address', AddressView.as_view(), name='address'),
]

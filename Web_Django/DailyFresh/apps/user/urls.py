from django.urls import path
from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView

app_name = "user"

urlpatterns = [
	path("register", RegisterView.as_view(), name="register"),
	path("active/<token>",ActiveView.as_view(), name="active"),
	path("login", LoginView.as_view(), name="login"),
	path("logout", LogoutView.as_view(), name="logout"),
	path("", UserInfoView.as_view(), name="user"),
	path("order", UserOrderView.as_view(), name="order"),
	path("address", AddressView.as_view(), name="address"),
]


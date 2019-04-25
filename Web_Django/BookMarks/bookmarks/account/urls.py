from django.urls import path
from .views import user_login, dashboard

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import logout_then_login, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = "account"

urlpatterns = [
	# path("login", user_login, name="login"),
	# django内置认证系统的方法
	path("login", LoginView.as_view(), name="login"),
	path("logout", LoginView.as_view(template_name="registration/logged_out.html"), name="logout"),
	path("logout-then-login", logout_then_login, name="logout_then_login"),
	path("password_change", PasswordChangeView.as_view(template_name="registration/password_change_form.html", success_url="/account/password_change/done"), name="password_change"),
	path("password_change/done", PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name="password_change_done"),
	path("password_reset", PasswordResetView.as_view(template_name="registration/password_reset_form.html", email_template_name="registration/password_reset_email.html", success_url="/account/password_reset/done"), name="password_reset"),
	path("password_reset/done", PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
	path("password_reset/confirm/<uidb64>/<token>", PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html", success_url="/account/password_reset/complete"), name="password_reset_confirm"),
	path("password_reset/complete", PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
	path("", dashboard, name="dashboard"),
]

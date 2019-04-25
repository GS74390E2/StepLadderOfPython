from django import forms


class LoginForm(forms.Form):
	"""登录表单"""
	username = forms.CharField()
	# 组件渲染
	password = forms.CharField(widget=forms.PasswordInput)


from django.shortcuts import render, reverse, redirect
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from user.models import User, Address
from goods.models import GoodsSKU
import re
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection


# Create your views here.


class RegisterView(View):
	"""注册"""
	def get(self, request):
		"""显示注册页面"""
		return render(request, "register.html")

	def post(self, request):
		"""注册处理"""
		# 1.接受数据
		username = request.POST.get("user_name")
		password = request.POST.get("pwd")
		email = request.POST.get("email")
		allow = request.POST.get("allow")

		# 2. 数据校验
		if not all([username, password, email]):
			return render(request, "register.html", {"errmsg": "数据不完整"})

		if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
			return render(request, "register.html", {"errmsg": "邮箱格式不正确"})

		if allow != "on":
			return render(request, "register.html", {"errmsg": "请同意协议"})

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			#  用户不存在
			user = None
		
		if user:
			return render(request, "register.html", {"errmsg": "用户名已存在"})

		# 用户注册
		user = User.objects.create_user(username, email, password)
		user.is_active = 0  # 未激活
		user.save()

		# 发送激活邮件
		serializer = Serializer(settings.SECRET_KEY, 3600)
		info = {"confirm": user.id}
		token = serializer.dumps(info)
		token = token.decode()

		# 邮件发送使用celery异步框架
		send_register_active_email.delay(email, username, token)

		# 返回应答, 反向解析跳转到首页
		return redirect(reverse("goods:index"))


class ActiveView(View):
	"""用户激活"""
	def get(self, request, token):
		"""用户激活"""
		serializer = Serializer(settings.SECRET_KEY, 3600)
		try:
			info = serializer.loads(token)
			user_id = info["confirm"]

			user = User.objects.get(id=user_id)
			user.is_active = 1
			user.save()

			return redirect(reverse("user:login"))
		except SignatureExpired as e:
			return HttpResponse("激活已过期")


class LoginView(View):
	"""登录"""
	def get(self, request):
		"""显示登录页面"""
		if "username" in request.COOKIES:
			username = request.COOKIES.get("username")
			checked = "checked"
		else:
			username = ""
			checked = ""

		return render(request, "login.html", {"username": username, "checked": checked})

	def post(self, request):
		"""登录校验"""
		# 1.接受数据
		username = request.POST.get("username")
		password = request.POST.get("pwd")

		# 2.校验数据
		if not all([username, password]):
			return render(request, "login.html", {"errmsg": "数据不完整"})

		# 3.业务处理
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				# 已激活用户, 注册登录状态到session
				login(request, user)

				# 登录后默认跳转到的地址
				next_url = request.GET.get("next", reverse("goods:index"))
				
				# 重定向
				response = redirect(next_url)

				remember = request.POST.get("remember")

				if remember == "on":
					# 记住用户名
					response.set_cookie("username", username, max_age=7 * 24 * 3600)
				else:
					response.delete_cookie("username")

				return response
			else:
				return render(request, "login.html", {"errmsg": "账户未激活"})
		else:
			return render(request, "login.html", {"errmsg": "用户名或者密码错误"})


class LogoutView(View):
	"""退出"""
	def get(self, request):
		# 消除session
		logout(request)

		return redirect(reverse("goods:index"))


class UserInfoView(LoginRequiredMixin, View):
	"""用户中心--信息页
		多继承, 先继承LoginMixin调用父类的as_view方法返回对象,
		再使用login_required包装"""
	def get(self, request):
		"""显示"""
		# Django 会给request对象添加一个属性request.user
		# 如果用户未登录则为AnonymousUser的一个实例
		user = request.user
		address = Address.objects.get_default_address(user)

		# 获取用户的历史浏览记录
		conn = get_redis_connection("default")
		history_key = "history_%d" % user.id

		# 获取用户最新浏览的5个商品id
		sku_ids = conn.lrange(history_key, 0, 4)

		# 便利获取用户浏览的商品信息
		goods_li = []
		for id in sku_ids:
			goods = GoodsSKU.objects.get(id=id)
			goods_li.append(goods)

		# 组织上下文
		context = {"page": "user", "address": address, "goods_li": goods_li}
		return render(request, "user_center_info.html", context)


class UserOrderView(LoginRequiredMixin, View):
	"""用户中心-- 订单页"""
	def get(self, request):
		"""显示"""
		return render(request, "user_center_order.html", {"page": "order"})


class AddressView(LoginRequiredMixin, View):
	"""用户中心-- 地址页"""
	def get(self, request):
		"""显示"""
		user = request.user

		try:
			address = Address.objects.get(user=user, is_default=True)
		except Address.DoesNotExist:
			address = None

		return render(request, "user_center_site.html", {"page": "address", "address": address})

	def post(self, request):
		"""地址添加"""
		# 接受数据
		receiver = request.POST.get("receiver")
		addr = request.POST.get("addr")
		zip_code = request.POST.get("zip_code")
		phone = request.POST.get("phone")

		# 校验数据
		if not all([receiver, addr, phone]):
			return render(request, "user_center_site.html", {"errmsg": "数据不完整"})

		# 校验手机号
		if not re.match(r"^1[3|4|5|7|8][0-9]{9}$", phone):
			return render(request, "user_center_site.html", {"errmsg": "手机号码格式错误"})

		user = request.user
		address = Address.objects.get_default_address(user)

		if address:
			is_default = False
		else:
			is_default = True

		# 添加地址
		Address.objects.create(user=user, receiver=receiver, addr=addr, zip_code=zip_code, phone=phone, is_default=is_default)

		return redirect(reverse("user:address"))


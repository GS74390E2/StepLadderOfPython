from django.shortcuts import render, redirect
from django.views.generic import View
import re
from django.urls import reverse
from user.models import User, Address
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from celery_tasks.tasks import send_register_active_email
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
from goods.models import GoodsSKU

# Create your views here.


class RegisterView(View):
    """注册类视图"""

    def get(self, request):
        """显示注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """进行注册处理"""
        # 1.接收数据
        user_name = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2.数据校验
        if not all([user_name, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            print('*' * 50)
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})

        # 用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 3.进行业务处理: 进行用户注册
        user = User.objects.create_user(user_name, email, password)
        user.is_active = 0
        user.save()

        # 4.发送激活邮件，包含激活链接:http://localhost:8000/user/active/id(加密)
        # 激活链接需要包含用户的身份信息，用户的身份信息需要加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode('utf-8')

        # 发邮件
        # send_register_active_email.delay(email, user_name, token)
        # 发送邮件到smtp服务器和smtp服务器到用户邮箱有时延，会在这里阻塞
        subject = '久违欢迎你'  # title
        message = ''  # content
        sender = settings.DEFAULT_FROM_EMAIL
        receiver = [email]
        html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员<h1>请点击下面链接激活您的账户<br />' \
                       '<a href="http://127.0.0.1:8000/user/active/%s">' \
                       'http://127.0.0.1:8000/user/active/%s</a>' % (user_name, token, token)
        send_mail(subject, message, sender, receiver, html_message=html_message)

        # 5.返回应答, 跳转到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """进行用户激活"""
        # 进行解密
        # print("-----------------:{}".format(token))
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登陆页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse("激活链接已过期")


class LoginView(View):
    """登陆"""

    def get(self, request):
        """显示登陆页面"""
        # 判断是否记住用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        return render(request, 'login.html', {"username": username, "checked": checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        # 校验数据
        if not all([username, password]):
            return render(request, "login.html", {"errmsg": "数据不完整"})

        # 登陆验证
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # 用户已激活
                login(request, user)

                # 获取登录后要跳转的地址
                next_url = request.GET.get("next", reverse("goods:index"))

                # 跳转到首页
                response = redirect(next_url)

                # 判断是否需要记住用户名
                remember = request.POST.get("remember", "")
                if remember == "on":
                    # 记住用户名
                    response.set_cookie("username", username, max_age=7*24*3600)
                else:
                    response.delete_cookie("username")
                return response
            else:
                # 用户未激活
                return render(request, "login.html", {"errmsg": "用户未激活"})
        else:
            return render(request, "login.html", {"errmsg": "用户名密码错误"})


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        """退出"""
        # 清楚用户session
        logout(request)

        # 调换到首页
        return redirect(reverse("goods:index"))


class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息页"""
    def get(self, request):
        """"""
        # django内置认证系统会拦截request进行登录校验, 设置属性request.user
        # 如果用户登录 -> User类的一个实例
        # 如果未登录 -> AnonymousUser类的一个实例
        # django会把request.user传给模板文件

        # 获取用户个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的历史浏览记录

        conn = get_redis_connection('default')
        history_key = 'history_%d' % user.id

        # 获取用户最新浏览的
        sku_ids = conn.lrange(history_key, 0, 4)

        # 从数据库查询用户浏览的商品信息
        goods_li = [GoodsSKU.objects.get(id=id) for id in sku_ids]

        # 组织上下文
        context = {"page": "user", "address": address, "goods_li": goods_li}

        return render(request, 'user_center_info.html', context)


class UserOrderView(LoginRequiredMixin, View):
    """用户中心-订单页"""
    def get(self, request):
        """"""
        # 获取用户的订单信息
        return render(request, 'user_center_order.html', {"page": "order"})


class AddressView(LoginRequiredMixin, View):
    """用户中心-地址页"""
    def get(self, request):
        """"""
        # 获取默认收货地址
        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        address = Address.objects.get_default_address(user)

        # 使用模板
        return render(request, 'user_center_site.html', {"page": "address", "address": address})

    def post(self, request):
        """地址添加"""
        # 接收数据
        receiver = request.POST.get("receiver")
        addr = request.POST.get("addr")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")

        # 校验
        if not all([receiver, addr, phone]):
            return render(request, "user_center_site.html", {"errmsg": "数据不完整"})

        if not re.match(r"1[3|4|5|7|8][0-9]{9}$", phone):
            return render(request, "user_center_site.html", {"errmsg": "手机号不合法"})

        # 业务处理
        user = request.user
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user, receiver=receiver, addr=addr, zip_code=zip_code, is_default=is_default)

        # 返回应答
        return redirect(reverse("user:address"))

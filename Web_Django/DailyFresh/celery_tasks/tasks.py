from django.core.mail import send_mail
from django.conf import settings
from django.template import loader, RequestContext
from celery import Celery
import time
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DailyFresh.settings')
django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from django_redis import get_redis_connection

# 创建一个Celery实例
app = Celery("celery_tasks.tasks", broker="")


@app.task
def send_register_active_email(to_email, username, token):
	"""发送激活邮件"""
	subject = "welcome to daily fresh"
	message = ""
	sender = settings.EMAIL_HOST_USER
	receiver = [to_email]
	html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://ip:port/user/active/%s">http://ip:port/user/active/%s</a>' % (username, token, token)
	try:
		send_mail(subject, message, sender, receiver, html_message=html_message)
	except Exception as e:
		print("send email failed: {}".format(e))


@app.task
def generate_static_index_html():
	"""产生首页静态页面"""
	# 获取商品种类信息
	types = GoodsType.objects.all()
	# 获取首页轮播商品信息
	goods_banners = IndexGoodsBanner.objects.all().order_by("index")
	# 获取首页促销活动信息
	promotion_banners = IndexPromotionBanner.objects.all().order_by("index")
	# 获取首页分类商品展示信息
	for type in types:
		# 图片展示信息
		image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by("index")
		# 文字展示信息
		title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by("index")

		type.image_banners = image_banners
		type.title_banners = title_banners
	
	# 组织模板上下文
	context = {"type": types, "goods_banners": goods_banners, "promotion_banners": promotion_banners}

	# 使用模板
	temp = loader.get_template("static_index.html")
	static_index_html = temp.render(context)
	save_path = os.path.join(settings.BASE_DIR, "static/index.html")
	with open(save_path, "w") as f:
		f.write(static_index_html)


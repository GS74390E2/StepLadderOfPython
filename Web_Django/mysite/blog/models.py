from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class PublishedManage(models.Manager):
	"""管理器类"""
	def get_queryset(self):
		"""get_queryset()会返回执行过的查询集"""
		return super(PublishedManage, self).get_queryset().filter(status='published')


class Post(models.Model):
	"""模型类"""
	STATUS_CHOICES = (
		("draft", "Draft"),
		("published", "Published"),
	)
	# 标题, sql中转化的varchar
	title = models.CharField(max_length=250)
	
	# 短标签(在url中使用), 只包含字母、数字、下划线或连接线
	# 参数代表日期唯一
	slug = models.SlugField(max_length=250, unique_for_date="publish")
	
	# 用户, 多对一关系需要在多的一方建立外键
	# django2 之后需要对外键添加约束on_delete
	author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
	
	# 主体
	body = models.TextField()

	# 发布时间
	publish = models.DateTimeField(default=timezone.now)

	# 创建时间, 两种参数互斥
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

	class Meta:
		# 包含一些元数据
		# 数据库查询结果默认返回按publish降序
		ordering = ("-publish", )
	
	def __str__(self):
		return self.title

	# 添加管理器, 否则为默认的objects
	objects = models.Manager()
	published = PublishedManage()

	def get_absolute_url(self):
		"""返回一个标准url"""
		return reverse('blog:post_detail', args=[
			self.publish.year,
			self.publish.strftime('%m'),
			self.publish.strftime('%d'),
			self.slug])


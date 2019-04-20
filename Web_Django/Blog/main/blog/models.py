from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.


class PublishedManager(models.Manager):
	"""管理器"""
	def get_queryset(self):
		"""按发布状态筛选"""
		return super(PublishedManager, self).get_queryset().filter(status="published")


class Post(models.Model):
	"""博客模型类"""
	STATUS_CHOICES = (
		("draft", "Draft"),
		("published", "Published"),
	)
	title = models.CharField(max_length=250)
	# 短标签, 只包含字母、数字、下划线、连接线
	# 参数代表使用日期
	slug = models.SlugField(max_length=250, unique_for_date="publish")
	# 外键(多对一 需要在多的模型类中添加)
	# 参数代表 User 到 Post 的反向关系名
	author = models.ForeignKey(User, related_name="blog_posts", on_delete=models.CASCADE)
	body = models.TextField()
	# 发布时间
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# choices参数代表字段值只能是给予参数中的一个
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
	# 标签
	tags = TaggableManager()

	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		db_table = "blog_post"
		# 按publish降序
		ordering = ("-publish", )
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		"""返回一个对象的标准url"""
		return reverse("blog:post_detail", args=[self.publish.year, self.publish.strftime("%m"), self.publish.strftime("%d"), self.slug])


class Comment(models.Model):
	"""评论模型类"""
	# 可以通过comment.post从一条评论获取对应post
	# 通过post.comments.all()来取回一个post的全部评论
	# 否则默认为comment_set
	post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		db_table = "blog_comment"
		ordering = ("created", )

	def __str__(self):
		return "Comment by {} on {}".format(self.name, self.post)


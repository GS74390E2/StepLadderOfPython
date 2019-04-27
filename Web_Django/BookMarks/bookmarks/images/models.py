from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.


class Image(models.Model):
	"""image"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="images_created", on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	# 图片的源url
	url = models.URLField()
	image = models.ImageField(upload_to="images/%Y/%m/%d")
	description = models.TextField(blank=True)
	# db_index为创建索引
	created = models.DateField(auto_now_add=True, db_index=True)
	# 多对多
	# 会新建一个联接表, 并提供多对多管理器
	user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
			super(Image, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("images:detail", args=(self.id, self.slug))


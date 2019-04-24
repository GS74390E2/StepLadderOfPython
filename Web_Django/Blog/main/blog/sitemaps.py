from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
	"""post站点地图"""
	# 修改频率
	changefreq = "weekly"
	# 关联性
	priority = 0.9
	
	def items(self):
		return Post.published.all()

	def lastmod(self, obj):
		return obj.publish


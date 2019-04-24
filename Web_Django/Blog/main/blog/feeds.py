from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
	"""post 内容聚合"""
	# RSS属性<title>
	title = "My Blog"
	# <link>
	link = "/blog/"
	# <description>
	description = "New posts of my blog."

	def items(self):
		# feed中的对象
		return Post.published.all()[:5]

	def item_title(self, item):
		# item返回值的属性
		return item.title

	def item_description(self, item):
		return truncatewords(item.body, 30)

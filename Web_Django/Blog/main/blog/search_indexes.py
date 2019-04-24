from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
	"""post索引, 告知haystack那些数据需要被编入搜索索引"""
	# 主要搜索字段
	text = indexes.CharField(document=True, use_template=True)
	# 参数代表, 该索引对应Post的publish字段
	publish = indexes.DateTimeField(model_attr="publish")

	def get_model(self):
		return Post

	def index_queryset(self, using=None):
		return self.get_model().published.all()


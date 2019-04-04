from django.contrib import admin
from blog.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	"""后台管理模型类"""
	# 后台管理页面展示序列
	list_display = ("title", "slug", "author", "publish", "status")
	# 右侧边栏过滤器, 通过指定字段过滤返回结果
	list_filter = ("status", "created", "publish", "author")
	# 搜索框, 搜索字段
	search_fields = ("title", "body")
	# add之后自动填充
	prepopulated_fields = {"slug": ("title", )}
	# 搜索控件
	raw_id_fields = ("author", )
	# 通过时间层的快速导航栏
	date_hierarchy = "publish"
	# 按列表字段排序
	ordering = ["status", "publish"]


admin.site.register(Post, PostAdmin)

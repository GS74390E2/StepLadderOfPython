from django.contrib import admin
from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
	"""博客后台管理类"""
	list_display = ("title", "slug", "author", "publish", "status")
	# 过滤器
	list_filter = ("status", "created", "publish", "author")
	# 搜索字段列
	search_fields = ("title", "body")
	# slug自动填充
	prepopulated_fields = {"slug": ("title", )}
	# 搜索控件
	raw_id_fields = ("author", )
	# 时间层快速导航
	date_hierarchy = "publish"
	# 排序
	ordering = ("status", "publish")

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
	"""评论后台管理"""
	list_display = ("name", "email", "post", "created", "active")
	list_filter = ("active", "created", "updated")
	search_fields = ("name", "email", "body")

admin.site.register(Comment, CommentAdmin)

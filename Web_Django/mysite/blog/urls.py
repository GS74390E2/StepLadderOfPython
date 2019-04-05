from django.urls import path, re_path  # django2 推荐使用
from blog.views import PostListView, post_detail

app_name = 'blog'
urlpatterns = [
	path('', PostListView.as_view(), name='post_list'),
	re_path('^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<post>\w+[-\w+]*)', post_detail, name='post_detail'),
]

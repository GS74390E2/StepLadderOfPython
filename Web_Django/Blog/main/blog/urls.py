from django.urls import path, re_path, include
from .views import post_list, post_detail, PostListView, post_share, post_search
from .feeds import LatestPostsFeed


app_name = "blog"
urlpatterns = [
	path("", post_list, name="post_list"),
	# path("", PostListView.as_view(), name="post_list"),
	re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)', post_detail, name='post_detail'),
	path("<int:post_id>/share", post_share, name="post_share"),
	path("tag/<str:tag_slug>", post_list, name="post_list_by_tag"),
	path("feed/", LatestPostsFeed(), name="post_feed"),
	path("search", post_search, name="post_search"),
]

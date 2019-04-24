from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 分页展示
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

# Create your views here.


class PostListView(ListView):
	"""列表视图"""
	# 查询集
	queryset = Post.published.all()
	# 指定上下文对象
	context_object_name = "posts"
	# 分页
	paginate_by = 3
	template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
	"""展示post"""
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

	# 将全部结果每页3个展示
	paginator = Paginator(object_list, 3)
	page = request.GET.get("page")
	try:
		# 获取请求的页码
		posts = paginator.page(page)
	except PageNotAnInteger:
		# 异常情况返回1
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, "blog/post/list.html", {"page": page, "posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
	"""post详情"""
	post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month, publish__day=day)
	
	comments = post.comments.filter(active=True)
	new_comment = None

	if request.method == "POST":
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# 创建评论对象, 但不存入db
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		# 空表单
		comment_form = CommentForm()

	# 参数获取一个简单list
	post_tags_ids = post.tags.values_list("id", flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")[:4]
	return render(request, "blog/post/detail.html", {"post": post, "comments": comments, "new_comment": new_comment, "comment_form": comment_form, "similar_posts": similar_posts})


def post_share(request, post_id):
	""""""
	post = get_object_or_404(Post, id=post_id, status="published")
	sent = False
	cd = None
	if request.method == "POST":
		# 根据post信息提交
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# 获取验证通过的字段
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = "{}({}) recommends you reading '{}'".format(cd["name"], cd["email"], post.title)
			message = "Read '{}' at {}\n\n{}\'s comments: {}".format(post.title, post_url, cd["name"], cd["comments"])
			send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
			sent = True
	else:
		# 显示空表单
		form = EmailPostForm()
	return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent, "cd": cd})


def post_search(request):
	"""搜索视图"""
	# 实例表单
	form = SearchForm()
	cd = None
	results = None
	total_results = 0
	if "query" in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			cd = form.cleaned_data
			# 为所有被编入索引的对象Post进行一次搜索
			# load_all 立刻加载所有在数据库中的关联对象
			results = SearchQuerySet().models(Post).filter(content=cd["query"]).load_all()
			total_results = results.count()
	
	return render(request, "blog/post/search.html", {"form": form, "cd": cd, "results": results, "total_results": total_results})

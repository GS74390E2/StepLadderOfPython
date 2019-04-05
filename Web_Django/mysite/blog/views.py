from django.shortcuts import render
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.


class PostListView(ListView):
	"""类视图（django内置的列表展示）"""
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'


def post_list(request):
	"""post列表"""
	object_list = Post.published.all()
	# 分页
	paginator = Paginator(object_list, 3)  # 每页3个
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# 如果page不是一个整型, 返回第一页
		posts = paginator.page(1)
	except EmptyPage:
		# 如果page越界了, 返回最后一页
		posts = paginator.page(paginator.num_page)
	return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
	"""post详情"""
	print("year: {}".format(year))
	print("month: {}".format(month))
	print("day: {}".format(day))
	print("post: {}".format(post))
	# get_object_or_404()会获取匹配参数的对象, 若没有则404
	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
	return render(request, 'blog/post/detail.html', {'post': post})

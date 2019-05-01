from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
	"""若用户未登录则重定向到默认url"""
	@classmethod
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)


from django import forms  # 内置表单框架
from .models import Comment


class EmailPostForm(forms.Form):
	"""邮件表单"""
	name = forms.CharField(max_length=25)
	# 自带校验
	email = forms.EmailField()
	to = forms.EmailField()
	# 参数widget 指定控件属性
	# 参数required false代表字段可选
	comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
	"""评论表单"""
	class Meta:
		# 指定模型类来构建表单
		model = Comment
		fields = ("name", "email", "body")

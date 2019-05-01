from django.db import models


class BaseModel(models.Model):
	"""模型抽象类"""
	# 参数auto_now_add和auto_now互斥
	create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
	update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
	# 实际业务中不能实际删除数据, 用此标记是否删除
	is_delete = models.BooleanField(default=False, verbose_name="删除标记")

	class Meta:
		# 说明是一个抽象模型类, 不会为此模型类建表
		abstract = True


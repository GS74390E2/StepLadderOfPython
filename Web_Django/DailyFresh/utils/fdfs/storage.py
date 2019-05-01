from django.core.files.storage import Storage  # django文件存储
from django.conf import settings
from fdfs_client.client import Fdfd_client


class FDFSStorage(Storage):
	"""fast dfs 文件存储类"""
	def __init__(self, client_conf=None, base_url=None):
		if client_conf is None:
			client_conf = settigns.FDFS_CLIENT_CONF
		self.client_conf = client_conf

		if base_url is None:
			base_url = settings.FDFS_URL
		self.base_url = base_url

	def _open(self, name, mode="rb"):
		"""打开文件时使用"""
		pass

	def _save(self, name, content):
		"""保存文件使用"""
		# name: 选择上传的文件名
		# content: 包含上传文件内容的File对象
		client = Fdfd_client(self.client_conf)

		# 上传文件到fast dfs系统
		res = client.upload_by_buffer(content.read())

		if res.get("status") != "Upload successed.":
			raise Exception("上传文件到fast dfs失败")

		filename = res.get("Remote file_id")
		return filename

	def exists(self, name):
		"""判断文件名是否可用"""
		return False

	def url(self, name):
		return self.base_url + name


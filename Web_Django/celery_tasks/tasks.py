# 使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import os

# 创建一个Celery的实例对象
app = Celery('celery_tasks.tasks', broker='redis://:gjy743902@127.0.0.1:6379/8')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyDjango.settings')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '久违欢迎你'  # title
    message = ''  # content
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员<h1>请点击下面链接激活您的账户<br />' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    print("sender: {}  receiver: {}".format(sender, receiver))
    try:
        send_mail(subject, message, sender, receiver, html_message=html_message)
        print("send_mail successfully")
    except Exception as e:
        print(e)


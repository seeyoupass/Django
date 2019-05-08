from celery import Celery
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
import time

# django环境的初始化，在任务处理者worker一端加以下几句
#windows下celery运行时先安装eventlet，然后启动 celery -A celery_tasks.tasks worker -l info -P eventlet
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()


app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/8')

@app.task
def send_register_active_email(to_email,username,token):

    #邮箱激活
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM  # 发送人
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员' \
                   '</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s' \
                   '</a>' % (username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)


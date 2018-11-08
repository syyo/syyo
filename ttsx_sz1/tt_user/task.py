import time
from celery import task
from django.conf import settings
from django.core.mail import send_mail

# 使用celery

@task
def sayhello():
    print('hello...')
    time.sleep(2)
    print('django...')

@task
def sendmail(uid, uemail):
    msg='<a href="http://127.0.0.1:8000/user/active%s/">点击激活</a>'%(uid)
    send_mail('天天生鲜用户激活','',settings.EMAIL_FROM,[uemail],html_message=msg)


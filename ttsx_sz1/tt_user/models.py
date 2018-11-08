
from django.db import models


class UserInfo(models.Model):
    # 用户表
    uname = models.CharField(max_length=20)  # 姓名
    upwd = models.CharField(max_length=40)  # 密码
    uemail = models.CharField(max_length=30)  # 邮件
    isValid = models.BooleanField(default=True)
    isActive = models.BooleanField(default=False)  # 激活状态


class UserAddressInfo(models.Model):
    # 地址表
    uname = models.CharField(max_length=20)  # 收件人
    uaddress = models.CharField(max_length=100)    # 收获地址
    uphone = models.CharField(max_length=11)  # 收件人电话
    user = models.ForeignKey('UserInfo')  # 用户表的外键

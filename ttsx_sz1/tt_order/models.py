#coding=utf-8
from django.db import models


class OrderInfo(models.Model):
    # 订单表
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('tt_user.UserInfo')
    odate = models.DateTimeField(auto_now_add=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150)


class OrderDetailInfo(models.Model):
    # 订单详情
    goods = models.ForeignKey('tt_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    # 价格
    price = models.DecimalField(max_digits=5,decimal_places=2)
    # 数量
    count = models.IntegerField()
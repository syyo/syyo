# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tt_user', '0001_initial'),
        ('tt_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='tt_goods.GoodsInfo')),
                ('user', models.ForeignKey(to='tt_user.UserInfo')),
            ],
        ),
    ]

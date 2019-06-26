# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from firetemplate.models import System

# Create your models here.


class Host(models.Model):
    host_name = models.CharField(max_length=30, verbose_name=u"主机Host名称")
    ip = models.GenericIPAddressField(verbose_name=u"IP地址")
    username = models.CharField(max_length=30, verbose_name=u"用户名")
    password = models.CharField(max_length=50, verbose_name=u"密码")
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u"操作系统")
    note = models.TextField(verbose_name=u"备注")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"主机配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

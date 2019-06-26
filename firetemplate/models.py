# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.db import models

from datetime import datetime

# Create your models here.


class System(models.Model):
    system_name = models.CharField(max_length=30, verbose_name=u"系统名")
    system_version = models.CharField(max_length=10, verbose_name=u"系统版本")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"操作系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.system_name + " " + self.system_version


class FirewallTemplate(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, verbose_name=u"操作系统")
    template_name = models.CharField(max_length=30, default="", verbose_name=u"模板名")
    config_message = models.TextField(verbose_name=u"配置模板")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"配置模板"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.template_name

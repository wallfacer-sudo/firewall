# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

from hosts.models import Host
from firetemplate.models import FirewallTemplate

# Create your models here.


class RuleList(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name=u"主机")
    firewall_template = models.ForeignKey(FirewallTemplate, on_delete=models.CASCADE, verbose_name=u"规则模板")
    template_value = models.CharField(max_length=40, verbose_name=u"模板值")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"规则列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.host.ip

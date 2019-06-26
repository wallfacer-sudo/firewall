# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Host

# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ['host_name', 'ip', 'system', 'add_time']
    search_fields = ['host_name', 'ip']
    list_filter = ['system']
    readonly_fields = ['add_time']


admin.site.register(Host, HostAdmin)

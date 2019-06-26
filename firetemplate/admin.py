# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import System, FirewallTemplate

# Register your models here.


class SystemAdmin(admin.ModelAdmin):
    list_display = ['system_name', 'system_version', 'add_time']
    search_fields = ['system_name', 'system_version']
    list_filter = ['system_name']
    readonly_fields = ['add_time']


class FirewallTemplateAdmin(admin.ModelAdmin):
    list_display = ['system', 'template_name', 'config_message', 'add_time']
    search_fields = ['system', 'config_message']
    list_filter = ['system']
    readonly_fields = ['add_time']


admin.site.site_header = u"IPv6 防火墙管理系统"
admin.site.site_title = u"IPv6 防火墙管理系统"
admin.site.register(System, SystemAdmin)
admin.site.register(FirewallTemplate, FirewallTemplateAdmin)

# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from monitor.models import Category, User, Plugin, Record, RecordQueue


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_users']

    def get_users(self, obj):
        return ' / '.join([p.nickname + ' (' + p.email + ')' for p in obj.user_set.all()])
    get_users.short_description = '监视用户'


class UserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'email', 'get_categories']

    def get_categories(self, obj):
        return ', '.join([p.name for p in obj.category.all()])
    get_categories.short_description = '监视分类'


def enable_plugin(modeladmin, request, queryset):
    queryset.update(status=True)
enable_plugin.short_description = '启用选中插件'


def disable_plugin(modeladmin, request, queryset):
    queryset.update(status=False)
disable_plugin.short_description = '禁用选中插件'


class PluginAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'iden', 'url', 'status']
    actions = [enable_plugin, disable_plugin]


class RecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'postdate', 'timestamp']


class RecordQueueAdmin(admin.ModelAdmin):
    list_display = ['record', 'plugin', 'category', 'user', 'sent', 'timestamp']


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Plugin, PluginAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RecordQueue, RecordQueueAdmin)

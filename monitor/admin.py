# -*- coding: utf-8 -*-

from django.contrib import admin

from monitor.models import Category, User, Plugin, Record, RecordQueue


class CategoryAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


class PluginAdmin(admin.ModelAdmin):
    pass


class RecordAdmin(admin.ModelAdmin):
    pass


class RecordQueueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Plugin, PluginAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(RecordQueue, RecordQueueAdmin)

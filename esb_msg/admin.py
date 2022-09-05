from django.contrib import admin

from .models import Service, Receiver
# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['id', 'value_event', 'comment_event', 'value_service', 'comment_service', 'is_lookup']

    # 点击此字段可进行跳转详情页
    list_display_links = ['value_event', 'comment_event']

    # 搜索字段
    search_fields = ['comment_service', 'comment_event']

    # 每页显示多少条记录
    list_per_page = 20

    # #不显示字段
    # exclude = ['id', 'gmt_created']

    # 侧边过滤器
    list_filter = ['comment_service', 'comment_event']


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['id', 'value', 'comment', 'desc', 'router_id']

    # 点击此字段可进行跳转详情页
    list_display_links = ['id', 'value', 'comment']

    # 搜索字段
    search_fields = ['id', 'value', 'comment']

    # 每页显示多少条记录
    list_per_page = 20

    # 不显示字段
    # exclude = ['gmt_created']

    # 侧边过滤器
    list_filter = ['id', 'value', 'comment']


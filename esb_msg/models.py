import datetime

from django.db import models
from .lib.SQLServer import SQLServer

# 全局连接
mssql = SQLServer(server="172.16.33.183", user="sa", password="Knt2020@lh", database="ESB_MSG-B")


# Create your models here.
# 消息标签
class MessageTagList(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='消息标签记录Id', help_text='消息标签记录Id')
    MSG_ID = models.UUIDField(null=False, blank=False, db_index=True, verbose_name='消息ID', help_text='消息ID')
    mtlTag = models.CharField(null=False, blank=False, max_length=50, verbose_name='标签', help_text='标签')
    mtlText = models.CharField(null=False, blank=False, max_length=50, verbose_name='标签内容描述',
                               help_text='标签内容描述')
    gmt_created = models.DateTimeField(null=False, blank=False, auto_now=True, verbose_name='记录时间',
                                       help_text='记录时间')

    class Meta:
        db_table = 'MessageTagList'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """重写保存逻辑"""
        # 使用指定数据库保存数据
        # using = 'esb_msg'
        # super().save(force_insert, force_update, using=using, update_fields=None)
        sql = 'insert into MessageTagList(MSG_ID, mtlTag, mtlText, gmt_created) values(%s, %s, %s, %s)'
        value = (self.MSG_ID, self.mtlTag, self.mtlText, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        mssql.exec_update(sql, value)
        return


class Service(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='主键id', help_text='主键id')
    value_service = models.CharField(null=False, blank=False, max_length=8, verbose_name='服务代码',
                                     help_text='服务代码')
    comment_service = models.CharField(null=False, blank=False, max_length=64, verbose_name='服务名称',
                                       help_text='服务名称')
    value_event = models.CharField(null=False, blank=False, unique=True, max_length=8, verbose_name='事件代码',
                                   help_text='事件代码')
    comment_event = models.CharField(null=False, blank=False, max_length=64, verbose_name='事件名称',
                                     help_text='事件名称')
    is_lookup = models.BooleanField(null=False, blank=False, default=0, verbose_name='查询标识',
                                    help_text='查询标识')
    gmt_created = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name='创建时间',
                                       help_text='创建时间')

    def __str__(self):
        return f'{self.comment_service}->{self.comment_event}({self.value_event})'

    class Meta:
        db_table = 'esb_service'
        verbose_name = "消息服务"
        verbose_name_plural = verbose_name


class Receiver(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='主键id', help_text='主键id')
    value = models.CharField(null=False, unique=True, blank=False, max_length=8, verbose_name='接收方id', help_text='接收方id')
    comment = models.CharField(null=False, blank=False, max_length=64, verbose_name='接收方代码', help_text='接收方代码')
    show_name = models.CharField(null=False, blank=False, max_length=64, verbose_name='接收方名称', help_text='接收方名称')
    router_id = models.CharField(null=False, blank=False, max_length=64, verbose_name='路由id', help_text='建议使用代码id',
                                 default='@com.alsoapp.esb.router.main.')
    api = models.TextField(blank=True, max_length=128, verbose_name='接收方api地址', help_text='接收平台数据的地址')
    gmt_created = models.DateTimeField(null=False, blank=False, auto_now_add=True, verbose_name='创建时间',
                                       help_text='创建时间')
    service_id = models.ManyToManyField(Service, verbose_name='订阅的服务', help_text='订阅服务列表', blank=True)

    def __str__(self):
        return f'{self.show_name}({self.value})'

    class Meta:
        db_table = 'esb_receiver'
        verbose_name = "系统厂商"
        verbose_name_plural = verbose_name

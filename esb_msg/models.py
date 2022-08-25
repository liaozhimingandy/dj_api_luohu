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
        using = 'esb_msg'
        # super().save(force_insert, force_update, using=using, update_fields=None)
        sql = 'insert into MessageTagList(MSG_ID, mtlTag, mtlText, gmt_created) values(%s, %s, %s, %s)'
        value = (self.MSG_ID, self.mtlTag, self.mtlText, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        mssql.ExecUpdate(sql, value)
        return

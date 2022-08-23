from django.db import models


# Create your models here.
# 消息标签
class MessageTagList(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name='消息标签记录Id', help_text='消息标签记录Id')
    MSG_ID = models.UUIDField(null=False, blank=False, db_index=True, verbose_name='消息ID', help_text='消息ID')
    mtlTag = models.CharField(null=False, blank=False, max_length=50, verbose_name='标签', help_text='标签')
    mtlText = models.CharField(null=False, blank=False, max_length=50, verbose_name='标签内容描述', help_text='标签内容描述')
    gmt_created = models.DateTimeField(null=False, blank=False, auto_now=True, verbose_name='记录时间', help_text='记录时间')

    class Meta:
        app_label = 'esb_msg'
        db_table = 'MessageTagList'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # 使用指定数据库保存数据
        using = 'esb_msg'
        super().save(force_insert, force_update, using, update_fields)

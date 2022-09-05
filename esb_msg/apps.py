from django.apps import AppConfig


class MsgEsbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'esb_msg'
    verbose_name = '消息服务'

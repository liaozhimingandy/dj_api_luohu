# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2022 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   @Author      : liaoz
#   @Project     : dj_api_luohu
#   @File Name   : serializer.py
#   @Created Date: 2022-08-22 18:06
#      @Software : PyCharm
#         @e-Mail: liaozhimingandy@qq.com
#   @Description :
#
# ======================================================================
from rest_framework import serializers
from .models import MessageTagList


class MessageTagListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTagList
        fields = "__all__"

    def save(self, **kwargs):
        # 使用指定数据库
        # kwargs.update({'using': 'esb_msg'})
        return super().save(**kwargs)


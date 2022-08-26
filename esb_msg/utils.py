# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# ======================================================================
#   Copyright (C) 2022 liaozhimingandy@qq.com Ltd. All Rights Reserved.
#
#   @Author      : zhiming
#   @Project     : dj_api_luohu
#   @File Name   : utils.py
#   @Created Date: 2022-08-22 22:47
#      @Software : PyCharm
#         @e-Mail: liaozhimingandy@qq.com
#   @Description :
#
# ======================================================================


class CommonParse:

    @staticmethod
    def parse_data_for_msg(data: dict) -> dict:
        """
        根据消息体来解析数据
        """
        tag_msg, tag_comment = '', ''

        server_code = data.get('service').get('serviceCode')

        # 检验申请单信息
        if server_code in ('S0038', 'S0039'):
            for d in data.get('message').get('LAB_APPLY'):
                if d.get('DATA_ELEMENT_EN_NAME', '') == 'BAR_CODE':
                    tag_msg = d.get('DATA_ELEMENT_VALUE', '')
                    tag_comment = d.get('DATA_ELEMENT_NAME', '')

        # 检验申请单查询
        elif server_code in ('S0040',):
            for d in data.get('query').get('LAB_APPLY'):
                if d.get('DATA_ELEMENT_EN_NAME', '') == 'BAR_CODE':
                    tag_msg = d.get('DATA_ELEMENT_VALUE', '')
                    tag_comment = d.get('DATA_ELEMENT_NAME', '')
        # 检查申请单信息新增/更新
        elif server_code in ('S0041', 'S0042'):
            for d in data.get('message', '').get('EXAM_APPLY'):
                if d.get('DATA_ELEMENT_EN_NAME', '') == 'PATIENT_ID':
                    tag_msg = d.get('DATA_ELEMENT_VALUE', '')
                    tag_comment = d.get('DATA_ELEMENT_NAME', '')
        # 检查申请查询
        elif server_code in ('S0043', ):
            for d in data.get('query').get('EXAM_APPLY'):
                if d.get('DATA_ELEMENT_EN_NAME', '') == 'PATIENT_ID':
                    tag_msg = d.get('DATA_ELEMENT_VALUE', '')
                    tag_comment = d.get('DATA_ELEMENT_NAME', '')

        return {'mtlTag': tag_msg, 'mtlText': tag_comment}

import datetime
import json

import pytz
from django.shortcuts import render

# Create your views here.
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from pymssql import OperationalError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import MessageTagList
from .serializer import MessageTagListsSerializer


from .utils import CommonParse


@api_view(['GET'])
def demo(request):
    data = {"code": 200, 'msg': "成功"}
    return Response(data)


class MessageTagListViewSet(viewsets.ViewSet):
    queryset = MessageTagList.objects.all()
    serializer_class = MessageTagListsSerializer

    @swagger_auto_schema(
        operation_id='make_tag_for_msg',
        operation_summary='消息标签',
        operation_description='为消息并且解析出标签',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description='交互消息体'
        ),
        manual_parameters=[
          openapi.Parameter('msg_id', openapi.IN_QUERY, description="消息id", type=openapi.TYPE_STRING, required=True)
        ],
        responses={201: '已保存', 401: '未认证', 500: '服务器内部错误'}
    )
    @action(detail=False, methods=['POST'], name='make_tag')
    def make_tag_for_msg(self, request):
        gmt_created = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T', timespec='seconds')
        # 判断消息体是否为空
        if not request.data:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'code': status.HTTP_204_NO_CONTENT,
                                                                     'msg': '需要交互消息', 'gmt_created': gmt_created})
        # 给消息打标签
        try:
            data = CommonParse.parse_data_for_msg(request.data)
        except (Exception, ) as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'code': status.HTTP_406_NOT_ACCEPTABLE,
                                                                         'msg': f'意外的json结构,解析失败,原因:{e}',
                                                                         'gmt_created': gmt_created})

        # 获取消息唯一id
        msg_id = request.GET.get('msg_id')

        # 批量反序列化,
        if data and isinstance(data, list):
            for item in data:
                item['MSG_ID'] = msg_id
                serializer = MessageTagListsSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                # 保存到数据库
                try:
                    serializer.save()
                except (OperationalError, ) as e:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE,
                                    data={'code': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': f'数据库连接失败->{e}',
                                          'gmt_created': gmt_created})

        return Response(status=status.HTTP_200_OK, data={'code': status.HTTP_201_CREATED, 'msg': '保存成功',
                                                         'gmt_created': gmt_created})

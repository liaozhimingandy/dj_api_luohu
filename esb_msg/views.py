import datetime
import json

import pytz
from django.shortcuts import render

# Create your views here.
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from pymssql import OperationalError, IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import MessageTagList, mssql, Receiver, Service
from .serializer import MessageTagListsSerializer, ServiceSerializer, ReceiverSerializer

from .utils import CommonParse


@api_view(['GET'])
def demo(request):
    data = {"code": 200, 'msg': "成功"}
    return Response(data)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ReceiverViewSet(viewsets.ModelViewSet):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer


class MessageTagListViewSet(viewsets.ViewSet):
    queryset = MessageTagList.objects.all()
    serializer_class = MessageTagListsSerializer

    @swagger_auto_schema(
        operation_id='make_tag_for_msg',
        operation_summary='消息标签',
        operation_description='为消息解析出标签并且保存',
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
        # 获取消息唯一id
        msg_id = request.GET.get('msg_id')
        gmt_created = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).isoformat(sep='T', timespec='seconds')

        # 判断消息体是否为空
        if not request.data:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'code': status.HTTP_204_NO_CONTENT,
                                                                     'msg': '需要交互消息', 'gmt_created': gmt_created})

        # 判断消息是否已处理
        sql = f"select count(1) [count] from MessageTagList(nolock) where msg_id='{msg_id}'"
        try:
            count = mssql.exec_query(sql)[0][0]
        except (OperationalError, IntegrityError) as e:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE,
                            data={'code': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': f'数据库处理失败->{e}',
                                  'gmt_created': gmt_created})
        if count:
            return Response(status=status.HTTP_202_ACCEPTED, data={'code': status.HTTP_202_ACCEPTED,
                                                                   'msg': '已处理过的消息,不再处理',
                                                                   'gmt_created': gmt_created})

        # 给消息打标签
        try:
            data = CommonParse.parse_data_for_msg(request.data)
        except (Exception,) as e:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'code': status.HTTP_406_NOT_ACCEPTABLE,
                                                                         'msg': f'意外的json结构,解析失败,原因:{e}',
                                                                         'gmt_created': gmt_created})
        # 判断是否解析到标签
        if not data:
            return Response(status=status.HTTP_202_ACCEPTED, data={'code': status.HTTP_202_ACCEPTED,
                                                                   'msg': f'已接收数据',
                                                                   'gmt_created': gmt_created})

        # list元素添加消息id
        # map(lambda item: item.update({'MSG_ID': msg_id}), data)
        for e in data:
            e.update({'MSG_ID': msg_id})

        # 批量反序列化并且保存到数据库
        serializer = MessageTagListsSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except (OperationalError, IntegrityError) as e:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE,
                            data={'code': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': f'数据库处理失败->{e}',
                                  'gmt_created': gmt_created})

        return Response(status=status.HTTP_200_OK, data={'code': status.HTTP_201_CREATED, 'msg': '保存成功',
                                                         'gmt_created': gmt_created})

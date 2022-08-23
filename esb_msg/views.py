import json

from django.shortcuts import render

# Create your views here.
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
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
        # 判断消息体是否为空
        if not request.data:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED, data={'code': 402, 'msg': '需要交互消息'})
        # 按需转换成json数据
        data = CommonParse.parse_data_for_msg(request.data)

        # 是否解析标签成功
        if data.get('mtlTag') == '':
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'code': 400, 'msg': '不需要解析的数据或未解析成功'})

        data['MSG_ID'] = request.GET.get('msg_id')

        # 反序列化
        serializer = MessageTagListsSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 保存到数据库
        serializer.save()
        return Response({'code': 200, 'msg': '保存成功'})

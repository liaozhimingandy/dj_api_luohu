import json

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import MessageTagList
from .serializer import MessageTagListsSerializer


def parse_data_for_msg(data: dict) -> dict:
    mtlTag, mtlText = '', ''
    for d in data.get('message').get('LAB_APPLY'):
        if d.get('DATA_ELEMENT_EN_NAME', '') == 'BAR_CODE':
            mtlTag = d.get('DATA_ELEMENT_VALUE', '')
            mtlText = d.get('DATA_ELEMENT_NAME', '')

            return {'mtlTag': mtlTag, 'mtlText': mtlText}

    return {}


@api_view(['GET'])
def demo(request):
    data = {"code": 200, 'msg': "成功"}
    return Response(data)


class MessageTagListViewSet(viewsets.ModelViewSet):
    queryset = MessageTagList.objects.all()
    serializer_class = MessageTagListsSerializer

    @action(detail=False, methods=['POST'], name='make_tag')
    def make_tag_for_msg(self, request):
        data = parse_data_for_msg(request.data)
        data['MSG_ID'] = request.GET.get('msg_id')

        serializer = MessageTagListsSerializer(data=data)
        serializer.is_valid()
        # 保存到数据库
        # serializer.save()
        return Response(data)

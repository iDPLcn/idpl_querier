# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from condor_archive.models import NodeInfo
from condor_archive.models import TransferTime
from condor_archive.serializers import NodeInfoSerializer
from condor_archive.serializers import TransferTimeSerializer
from datetime import datetime
from django.core.context_processors import request
from rest_framework.parsers import JSONParser
# Create your views here.

__all__ = ['NodeInfoView', 'TransferTimeView']

class NodeInfoView(APIView):
    '''
    Get all Node infomation
    '''

    def get(self, reqeust):
        nodeInfoList = NodeInfo.objects.all()
        serializer = NodeInfoSerializer(nodeInfoList, many=True)
        return Response(serializer.data)
    
class TransferTimeView(APIView):
    '''
    Get transfer time by hostname of source and destination, and time range
    src -- hostname of source
    dst -- hostname of destination
    timeStart -- start time
    timeEnd -- end time
    timeEnd-start -- start unixtime of timeEnd
    timeEnd-end -- end unixtime of timeEnd
    md5_equal -- md5 checksum is right
    duration -- timeEnd - timeStart
    '''
    
    def get(self, request):
        try:
            src = request.GET.get('src', '')
            dst = request.GET.get('dst', '')
            timeStart = float(request.GET.get('timeEnd-start', ''))
            timeEnd = float(request.GET.get('timeEnd-end', ''))
        except Exception:
            raise Http404
        TransferTimeList = TransferTime.objects.filter(
            source=src,
            destination=dst,
            time_end__gte=timeStart,
            time_end__lte=timeEnd
        )
        serializer = TransferTimeSerializer(TransferTimeList, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TransferTimeSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
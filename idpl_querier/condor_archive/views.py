# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from condor_archive.models import NodeInfo
from condor_archive.models import TransferTime
from condor_archive.serializers import NodeInfoSerializer
from condor_archive.serializers import TransferTimeSerializer
from datetime import datetime
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
    timeEnd-start -- start unixtime of timeEnd
    timeEnd-end -- end unixtime of timeEnd
    '''
    
    def get(self, request):
        try:
            src = request.GET.get('src', '')
            dst = request.GET.get('dst', '')
            timeStartStr = request.GET.get('timeEnd-start', '')
            timeEndStr = request.GET.get('timeEnd-end', '')
            timeStart = datetime.fromtimestamp(int(timeStartStr))
            timeEnd = datetime.fromtimestamp(int(timeEndStr))
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
# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from condor_archive.models import NodeInfo
from condor_archive.models import getTransferTimeModel
from condor_archive.serializers import NodeInfoSerializer
from condor_archive.serializers import TransferTimeSerializer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import APIException
from rest_framework import permissions
# Create your views here.

__all__ = ['NodeInfoView', 'TransferTimeView']

class ParameterError(APIException):
        
    status_code = 400
    detail = 'parameters error'

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request):
        src = request.GET.get('source', '')
        dst = request.GET.get('destination', '')
        organization = request.GET.get('organization', 'null')
        timeStartStr = request.GET.get('timeEnd-start')
        timeEndStr = request.GET.get('timeEnd-end')
        nodeInfoList = NodeInfo.objects.get(organization=organization)
        if not nodeInfoList:
            organization = 'null'
        try:
            timeStart = float(timeStartStr)
            timeEnd = float(timeEndStr)
        except Exception:
            raise ParameterError(detail='time parameters error')
        try:
            TransferTime = getTransferTimeModel(organization.lower())
            TransferTimeList = TransferTime.objects.filter(
                source=src,
                destination=dst,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            )
        except Exception:
            raise Http404
        serializer = TransferTimeSerializer(TransferTimeList, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = TransferTimeSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
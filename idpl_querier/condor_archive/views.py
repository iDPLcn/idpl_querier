# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from condor_archive.models import NodeInfo, MeasurePair
from condor_archive.models import getTransferTimeModel
from condor_archive.models import IperfTime
from condor_archive.models import NetcatData
from condor_archive.serializers import NodeInfoSerializer
from condor_archive.serializers import MeasurePairSerializer
from condor_archive.serializers import TransferTimeSerializer
from condor_archive.serializers import IperfTimeSerializer
from condor_archive.serializers import NetcatDataSerializer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import APIException
from rest_framework import permissions
from condor_archive.serializers import getOrganizationBySource
from datetime import datetime
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

__all__ = ['NodeInfoView', 'TransferTimeView', 'TransferTimeAvgView',
           'MeasurePairView', 'IperfTimeView', 'IperfTimeAvgView',
           'NetcatDataView', 'NetcatDataAvgView']

class ParameterError(APIException):

    status_code = 400
    detail = 'parameters error'

class NodeInfoView(APIView):
    '''
    Get all Node infomation
    '''

    def get(self, request):
        pool_no = request.GET.get('pool_no', '')
        if pool_no:
            nodeInfoList = NodeInfo.objects.filter(pool_no=pool_no)
        else:
            nodeInfoList = NodeInfo.objects.all()
        serializer = NodeInfoSerializer(nodeInfoList, many=True)
        return Response(serializer.data)
    
class MeasurePairView(APIView):
    '''
    Get all measurement pair
    '''
    
    def get(self, requset):
        measurePairList = MeasurePair.objects.all()
        serializer = MeasurePairSerializer(measurePairList, many=True)
        return Response(serializer.data)
    
class TransferTimeView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request):
        '''
        Get transfer time by source and destination, time range, organization
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        timeStartStr = request.GET.get('timeEnd-start')
        timeEndStr = request.GET.get('timeEnd-end')
        organization = getOrganizationBySource(source)
        try:
            timeStart = float(timeStartStr)
            timeEnd = float(timeEndStr)
        except Exception:
            raise ParameterError(detail='parameters format error')
        try:
            TransferTime = getTransferTimeModel(organization.lower())
            TransferTimeList = TransferTime.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).order_by('time_end')
        except Exception:
            raise Http404
        serializer = TransferTimeSerializer(TransferTimeList, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a transfer time object from JSON string, authentication needed
        """
        try:
            data = JSONParser().parse(request)
            update_measurepair(data['source'], data['destination'])
            serializer = TransferTimeSerializer(data=data)
            if serializer.is_valid():
                serializer.create(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            raise ParameterError(detail='parameters format error')
        
class TransferTimeAvgView(APIView):
    def get(self, request):
        '''
        Get average transfer time of the latest year by source and destination
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        organization = getOrganizationBySource(source)
        timeEnd = datetime.now()
        timeStart = datetime(timeEnd.year, 1, 1)
        try:
            TransferTime = getTransferTimeModel(organization.lower())
            TransferTimeAvg = TransferTime.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).aggregate(Avg('duration'))
        except Exception:
            raise Http404
        return Response(TransferTimeAvg)
    
class IperfTimeView(APIView):
    def get(self, request):
        '''
        Get iperf time by source and destination, time range, organization
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        timeStartStr = request.GET.get('timeEnd-start')
        timeEndStr = request.GET.get('timeEnd-end')
        try:
            timeStart = float(timeStartStr)
            timeEnd = float(timeEndStr)
        except Exception:
            raise ParameterError(detail='parameters format error')
        try:
            IperfTimeList = IperfTime.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).order_by('time_end')
        except Exception:
            raise Http404
        serializer = IperfTimeSerializer(IperfTimeList, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a iperf time object from JSON string, authentication needed
        """
        try:
            data = JSONParser().parse(request)
            update_measurepair(data['source'], data['destination'])
            serializer = IperfTimeSerializer(data=data)
            if serializer.is_valid():
                serializer.create(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            raise ParameterError(detail='parameters format error')
        
class IperfTimeAvgView(APIView):
    def get(self, request):
        '''
        Get average iperf bandwidth of the latest year by source and destination
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        timeEnd = datetime.now()
        timeStart = datetime(timeEnd.year, 1, 1)
        try:
            iperfBandwidthAvg = IperfTime.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).aggregate(Avg('bandwidth'))
        except Exception:
            raise Http404
        return Response(iperfBandwidthAvg)
    
class NetcatDataView(APIView):
    def get(self, request):
        '''
        Get netcat data by source and destination, time range, organization
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        timeStartStr = request.GET.get('timeEnd-start')
        timeEndStr = request.GET.get('timeEnd-end')
        try:
            timeStart = float(timeStartStr)
            timeEnd = float(timeEndStr)
        except Exception:
            raise ParameterError(detail='parameters format error')
        try:
            NetcatDataList = NetcatData.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).order_by('time_end')
        except Exception:
            raise Http404
        serializer = NetcatDataSerializer(NetcatDataList, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a netcat data object from JSON string, authentication needed
        """
        try:
            data = JSONParser().parse(request)
            update_measurepair(data['source'], data['destination'])
            serializer = NetcatDataSerializer(data=data)
            if serializer.is_valid():
                serializer.create(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            raise ParameterError(detail='parameters format error')

class NetcatDataAvgView(APIView):
    def get(self, request):
        '''
        Get average netcat bandwidth of the latest year by source and destination
        '''
        source = request.GET.get('source', '')
        destination = request.GET.get('destination', '')
        timeEnd = datetime.now()
        timeStart = datetime(timeEnd.year, 1, 1)
        try:
            netcatBandwidthAvg = NetcatData.objects.filter(
                source=source,
                destination=destination,
                time_end__gte=timeStart,
                time_end__lte=timeEnd
            ).aggregate(Avg('bandwidth'))
        except Exception:
            raise Http404
        return Response(netcatBandwidthAvg)
    
def update_measurepair(source_host, destination_host):
    try:
        source_node = NodeInfo.objects.get(host=source_host)
        destination_node = NodeInfo.objects.get(host=destination_host)
    except ObjectDoesNotExist:
        return None
    try:
        measurepair = MeasurePair.objects.get(
            source=source_node,
            destination=destination_node
        )
        return measurepair
    except ObjectDoesNotExist:
        measurepair = MeasurePair.objects.create(
            source=source_node,
            destination=destination_node
        )
        measurepair.save()
    finally:
        return measurepair
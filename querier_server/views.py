# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from esmond_client.connector import EsmondConn
from querier_server.serializers import IntFloatPointSerializer

# Create your views here.

__all__ = ['ThroughputQuerier', 'OwdelayQuerier', 'PingQuerier', 'LossQuerier']

class NetworkQuerier(APIView):

    def __getRequest(self, request):
        try:
            self.src = request.GET['src']
            self.dst = request.GET['dst']
            self.timeStart = request.GET['time-start']
            self.timeEnd = request.GET['time-end']
        except Exception:
            raise Http404
        
    def response(self, request, type):
        self.__getRequest(request)
        try:
            points = []
            conn = EsmondConn(self.src)
            if type == 'throughput':
                points = conn.getThroughputData(self.dst, self.timeStart, self.timeEnd)
            elif type == 'owdelay':
                points = conn.getOwdelayData(self.dst, self.timeStart, self.timeEnd)
            elif type == 'ping':
                points = conn.getPingData(self.dst, self.timeStart, self.timeEnd)
            elif type == 'loss':
                points = conn.getLossData(self.dst, self.timeStart, self.timeEnd)
            serializer = IntFloatPointSerializer(points, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
class ThroughputQuerier(NetworkQuerier):
    '''
    Get throughput data by src, dest and time range.
    '''
    
    def get(self, request):
        return self.response(request, 'throughput')
    
class OwdelayQuerier(NetworkQuerier):
    '''
    Get one-way delay data by src, dest and time range.
    '''
    
    def get(self, request):
        return self.response(request, 'owdelay')
    
class PingQuerier(NetworkQuerier):
    '''
    Get ping latency data by src, dest and time range.
    '''
    
    def get(self, request):
        return self.response(request, 'ping')
    
class LossQuerier(NetworkQuerier):
    '''
    Get loss rate data by src, dest and time range.
    '''
    
    def get(self, request):
        return self.response(request, 'loss')
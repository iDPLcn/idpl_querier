# from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from esmond_client.connector import EsmondConn
from querier_server.serializers import IntFloatPointSerializer

# Create your views here.

class ThroughputQuerier(APIView):
    '''
    Get throughput data by src, dest and time range.
    '''

    def __getRequest(self, request):
        try:
            self.src = request.GET['src']
            self.dst = request.GET['dst']
            self.timeStart = request.GET['timeStart']
            self.timeEnd = request.GET['timeEnd']
        except Exception:
            raise Http404
        
    def get(self, request):
        self.__getRequest(request)
        try:
            conn = EsmondConn(self.src)
            throughputs = conn.getThroughputData(self.dst, self.timeStart, self.timeEnd)
            serializer = IntFloatPointSerializer(throughputs, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
'''
Created on 2014.10.23

@author: Jarvis Zhang
'''

from rest_framework import serializers

class ThroughputSerializer(serializers.Serializer):
    timestamp = serializers.IntegerField()
    bandwidth = serializers.FloatField() 

'''
Created on 2014.10.23

@author: Jarvis Zhang
'''
from datetime import datetime
from rest_framework import serializers
from condor_archive.models import TransferTime

class UnixTimestampField(serializers.DateTimeField):
    
    def __init__(self, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        
    def to_native(self, value):
        return str(value.timestamp())
    
    def from_native(self, value):
        dt_value = datetime.fromtimestamp(value)
        return serializers.DateTimeField.from_native(self, dt_value)

class NodeInfoSerializer(serializers.Serializer):
    host = serializers.CharField()
    ip_address = serializers.CharField(max_length=39)
    organization = serializers.CharField()

class TransferTimeSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=64)
    destination = serializers.CharField(max_length=64)
    time_start = UnixTimestampField()
    time_end = UnixTimestampField()
    md5_equal = serializers.BooleanField()
    duration = serializers.IntegerField()
    
    def create(self, validated_data):
        """
        Create and return a new 'TransferTime' instance, given the validated data
        """
        return TransferTime.objects.create(**validated_data)
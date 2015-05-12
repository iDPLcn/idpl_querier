'''
Created on 2014.10.23

@author: Jarvis Zhang
'''
from datetime import datetime
from rest_framework import serializers
from condor_archive.models import getTransferTimeModel, NetcatData
from condor_archive.models import NodeInfo, MeasurePair, IperfTime
from django.core.exceptions import ObjectDoesNotExist

def getOrganizationBySource(source):
    try:
        nodeInfo = NodeInfo.objects.get(host=source)
        organization = nodeInfo.organization
    except ObjectDoesNotExist:
        organization = 'null'
    return organization


class UnixTimestampField(serializers.DateTimeField):
    
    def __init__(self, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        
    def to_native(self, value):
        return value.timestamp()
    
    def from_native(self, value):
        dt_value = datetime.fromtimestamp(float(value))
        return serializers.DateTimeField.from_native(self, dt_value)

class NodeInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NodeInfo
        field = ('id', 'host', 'ip_address', 'organization', 'pool_no')
    
class MeasurePairSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MeasurePair
        field = ('id', 'source', 'destination')
                
MeasurePairSerializer.base_fields['source'] = NodeInfoSerializer()
MeasurePairSerializer.base_fields['destination'] = NodeInfoSerializer()

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
        source = validated_data.get('source', '')
        organization = getOrganizationBySource(source)
        
        TransferTime = getTransferTimeModel(organization.lower())
        return TransferTime.objects.create(**validated_data)
    
class IperfTimeSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=64)
    destination = serializers.CharField(max_length=64)
    time_start = UnixTimestampField()
    time_end = UnixTimestampField()
    md5_equal = serializers.BooleanField()
    duration = serializers.FloatField()
    data_size = serializers.FloatField()
    bandwidth = serializers.FloatField()
    
    def create(self, validated_data):
        """
        Create and return a new 'IperfTime' instance, given the validated data
        """
        return IperfTime.objects.create(**validated_data)
    
class NetcatDataSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=64)
    destination = serializers.CharField(max_length=64)
    time_start = UnixTimestampField()
    time_end = UnixTimestampField()
    md5_equal = serializers.BooleanField()
    duration = serializers.FloatField()
    data_size = serializers.FloatField()
    bandwidth = serializers.FloatField()
    
    def create(self, validated_data):
        """
        Create and return a new 'NetcatData' instance, given the validated data
        """
        return NetcatData.objects.create(**validated_data)
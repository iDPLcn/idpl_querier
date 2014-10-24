'''
Created on 2014.10.23

@author: Jarvis Zhang
'''

from rest_framework import serializers

class IntFloatPointSerializer(serializers.Serializer):
    x_value = serializers.IntegerField()
    y_value = serializers.FloatField() 

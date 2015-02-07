from django.contrib import admin
from condor_archive.models import NodeInfo
from condor_archive.models import MeasurePair
# Register your models here.

class NodeInfoAdmin(admin.ModelAdmin):
    field = ['host', 'ip_address', 'organization']
    list_display = ['host', 'organization']
    
class MeasurePairAdmin(admin.ModelAdmin):
    field = ['source', 'destination']
    list_display=['get_source_host', 'get_destination_host']
    
    def get_source_host(self, obj):
        return obj.source.host
    
    def get_destination_host(self, obj):
        return obj.destination.host
    
    get_source_host.short_description='source'
    get_destination_host.short_description='destination'
    
admin.site.register(NodeInfo, NodeInfoAdmin)
admin.site.register(MeasurePair, MeasurePairAdmin)
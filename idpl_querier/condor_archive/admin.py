from django.contrib import admin
from condor_archive.models import NodeInfo
from condor_archive.models import MeasurePair
# Register your models here.

class NodeInfoAdmin(admin.ModelAdmin):
    field = ['host', 'ip_address', 'organization']
    
class MeasurePairAdmin(admin.ModelAdmin):
    field = ['source', 'destination']
    
admin.site.register(NodeInfo, NodeInfoAdmin)
admin.site.register(MeasurePair, MeasurePairAdmin)
from django.contrib import admin
from condor_archive.models import NodeInfo

# Register your models here.

class NodeInfoAdmin(admin.ModelAdmin):
    field = ['host', 'ip_address', 'organization']
    
admin.site.register(NodeInfo, NodeInfoAdmin)
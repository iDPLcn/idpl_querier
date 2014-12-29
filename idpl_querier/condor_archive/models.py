from django.db import models
from time import strftime
from datetime import datetime

# Create your models here.   
class NodeInfo(models.Model):
    host = models.TextField()
    ip_address = models.GenericIPAddressField(null=False)
    organization = models.TextField()
    
    class Meta:
        db_table = "NODE_INFO"
        
class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the 
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """ 
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1 
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())
    
class TransferTime(models.Model):
    source = models.CharField(max_length=64, null=False)
    destination = models.CharField(max_length=64, null=False)
    time_start = UnixTimestampField(null=False)
    time_end = UnixTimestampField(null=False)
    md5_equal = models.BooleanField(null=False, default=None)
    duration = models.PositiveIntegerField(null=False)
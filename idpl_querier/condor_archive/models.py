from django.db import models
from time import strftime
from datetime import datetime

__all__ = ['NodeInfo', 'MeasurementInfo', 'MeasurementData', 'MeasurePair', 
           'IperfTime', 'NetcatData', 'getTransferTimeModel']

# Create your models here.
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
        if isinstance(value, int) or isinstance(value, float):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        elif isinstance(value, float) or isinstance(value, int):
            value = datetime.fromtimestamp(value)
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())

class NodeInfo(models.Model):
    host = models.TextField()
    ip_address = models.GenericIPAddressField(null=False)
    organization = models.TextField()
    pool_no = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        db_table = 'NODE_INFO'
        
    def __str__(self):
        return self.host

class MeasurementInfo(models.Model):
    tool_name = models.TextField(null=False)
    
    class Meta:
        db_table = 'MEASUREMENT_INFO'
        
    def __str__(self):
        return self.tool_name
    
    def __unicode__(self):
        return self.tool_name

class MeasurementData(models.Model):
    source = models.CharField(max_length=64, null=False)
    destination = models.CharField(max_length=64, null=False)
    time_start = UnixTimestampField(null=False)
    time_end = UnixTimestampField(null=False)
    md5_equal = models.BooleanField(null=False, default=None)
    duration = models.FloatField(null=False)
    data_size = models.FloatField(null=False)
    bandwidth = models.FloatField(null=False)
    measurement = models.ForeignKey(MeasurementInfo, related_name='measurements')

class MeasurePair(models.Model):
    source = models.ForeignKey(NodeInfo, related_name='source_measurepairs')
    destination = models.ForeignKey(NodeInfo,
                                    related_name='destination_measurepairs')


class TransferTime(models.Model):
    '''
        Deprecated, new model is MeasurementData
    '''
    source = models.CharField(max_length=64, null=False)
    destination = models.CharField(max_length=64, null=False)
    time_start = UnixTimestampField(null=False)
    time_end = UnixTimestampField(null=False)
    md5_equal = models.BooleanField(null=False, default=None)
    duration = models.PositiveIntegerField(null=False)
    
    class Meta:
        abstract = True
        app_label = 'condor_archive'
        managed = False

class IperfTime(models.Model):
    '''
        Deprecated, new model is MeasurementData
    '''
    source = models.CharField(max_length=64, null=False)
    destination = models.CharField(max_length=64, null=False)
    time_start = UnixTimestampField(null=False)
    time_end = UnixTimestampField(null=False)
    md5_equal = models.BooleanField(null=False, default=None)
    duration = models.FloatField(null=False)
    data_size = models.FloatField(null=False)
    bandwidth = models.FloatField(null=False)
    
class NetcatData(models.Model):
    '''
        Deprecated, new model is MeasurementData
    '''
    source = models.CharField(max_length=64, null=False)
    destination = models.CharField(max_length=64, null=False)
    time_start = UnixTimestampField(null=False)
    time_end = UnixTimestampField(null=False)
    md5_equal = models.BooleanField(null=False, default=None)
    duration = models.FloatField(null=False)
    data_size = models.FloatField(null=False)
    bandwidth = models.FloatField(null=False)

def getTransferTimeModel(organization, BaseClass = TransferTime):
    if organization in globals():
        return globals()[organization]
    table_name_prefix = 'condor_archive_transfertime'
    table_name = '{0}_{1}'.format(table_name_prefix, organization)

    class NewMeta:
        app_label = 'condor_archive'
        managed = False
        db_table = table_name
    
    newClass = type(
        table_name,
        (BaseClass,),
        {
            'Meta': NewMeta,
            '__module__': __name__,
        }
    )
    globals()[organization] = newClass
    return newClass
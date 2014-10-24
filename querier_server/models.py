from django.db import models

# Create your models here.

class Throughput(models.Model):
    timestamp = models.IntegerField();
    bandwidth = models.FloatField();
    
    def __init__(self, timestamp, bandwidth):
        self.timestamp = timestamp
        self.bandwidth = bandwidth
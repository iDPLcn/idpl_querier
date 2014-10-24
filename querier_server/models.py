from django.db import models

# Create your models here.

class IntFloatPoint(models.Model):
    x_value = models.IntegerField();
    y_value = models.FloatField();
    
    def __init__(self, x_value, y_value):
        self.x_value = x_value
        self.y_value = y_value
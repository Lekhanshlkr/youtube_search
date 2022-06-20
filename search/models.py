from django.db import models

class Videos(models.Model):
    title = models.CharField(null=True,blank=True,max_length=500)
    duration = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=8)
    date = models.DateTimeField()
    thumbnail = models.URLField()
    description = models.CharField(null=True,blank=True,max_length=6000)


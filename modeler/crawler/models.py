from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField()

class Data(models.Model):
    url = models.URLField()
    content = models.TextField()
    date = models.DateTimeField()
    tags = models.TextField()
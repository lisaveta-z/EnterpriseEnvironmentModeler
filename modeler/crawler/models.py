from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField()
    additional_url = models.URLField(blank=True)

class Data(models.Model):
    url = models.URLField()
    title = models.TextField(blank=True)
    content = models.TextField()
    date = models.DateTimeField()
    tags = models.TextField()
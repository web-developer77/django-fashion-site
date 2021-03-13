from django.db import models

class trends(models.Model):
    name = models.CharField(max_length=75)
    brand = models.CharField(max_length=50)
    image = models.FileField(upload_to='user_image')
    url = models.URLField()
    active = models.BooleanField(default=True)

class feedback(models.Model):
    userid = models.IntegerField()
    feed = models.CharField(max_length=200)
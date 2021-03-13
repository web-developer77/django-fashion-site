from django.db import models
from django.contrib.auth.models import User
gen = (
    ('M','Male'),
    ('F','Female'),
    ('O','Prefer not to say'),
)
skin = (
    ('1','Fair'),
    ('2','Olive'),
    ('3','Brown'),
    ('4','Black'),
)
hair = (
    ('black','black'),
    ('brown','brown'),
    ('Blond','Blonde'),
    ('Red','Red'),
    ('White/Gray','White/Gray'),
)
class trends(models.Model):
    name = models.CharField(max_length=75)
    brand = models.CharField(max_length=50)
    image = models.FileField(upload_to='user_image')
    url = models.URLField()
    active = models.BooleanField(default=True)

class feedback(models.Model):
    userid = models.IntegerField()
    feed = models.CharField(max_length=200)

class CustInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(choices=gen,max_length=50)
    skintone = models.CharField(choices=skin,max_length=50)
    height = models.CharField(max_length=75)
    weight = models.CharField(max_length=75)
    haircolors = models.CharField(choices=hair,max_length=50)
    mobno = models.IntegerField()
    age = models.IntegerField()

class EmployeeInfo(models.Model):
    user = models.IntegerField(primary_key=True)
    gender = models.CharField(choices=gen,max_length=50)
    mobno = models.IntegerField()
    age = models.IntegerField()
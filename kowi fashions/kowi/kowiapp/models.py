from django.db import models
from django.contrib.auth.models import User
gen = (
    ('Male','Male'),
    ('Female','Female'),
    ('Prefer not to say','Prefer not to say'),
)
skin = (
    ('Fair','Fair'),
    ('Olive','Olive'),
    ('Brown','Brown'),
    ('Black','Black'),
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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Manage Trends"

class feedback(models.Model):
    userid = models.IntegerField()
    feed = models.CharField(max_length=200)

    def __str__(self):
        us = User.objects.get(id=self.userid)
        return "Feedback by: "+us.username

    class Meta:
        verbose_name_plural = "Feedback by Users"

class CustInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(choices=gen,max_length=50)
    skintone = models.CharField(choices=skin,max_length=50)
    height = models.CharField(max_length=75)
    weight = models.CharField(max_length=75)
    haircolors = models.CharField(choices=hair,max_length=50)
    mobno = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        us = User.objects.get(id=self.id)
        return "Customer Name: "+us.username
    
    class Meta:
        verbose_name_plural = "Customer's Information"

class EmployeeInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(choices=gen,max_length=50)
    mobno = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        us = User.objects.get(id=self.id)
        return "Employee Name: "+us.username
    
    class Meta:
        verbose_name_plural = "Employee's Information"
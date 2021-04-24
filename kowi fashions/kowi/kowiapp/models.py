from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


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
    mobno = models.IntegerField(blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    lat = models.DecimalField(max_digits = 9, decimal_places = 6,blank=True,null=True)
    lng = models.DecimalField(max_digits = 9, decimal_places = 6,blank=True,null=True)

    def __str__(self):
        us = User.objects.get(id=self.id)
        return "Customer Name: "+us.username
    
    class Meta:
        verbose_name_plural = "Customer's Information"

class EmployeeInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(choices=gen,max_length=50)
    mobno = models.IntegerField(blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    lat = models.DecimalField(max_digits = 9, decimal_places = 6,blank=True,null=True)
    lng = models.DecimalField(max_digits = 9, decimal_places = 6,blank=True,null=True)

    def __str__(self):
        us = User.objects.get(id=self.id)
        return "Employee Name: "+us.username
    
    class Meta:
        verbose_name_plural = "Employee's Information"


class Author(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	rate = models.IntegerField(default=0)
	def __str__(self):
		return f'{self.user}'

class Post(models.Model):
	title = models.CharField(max_length = 50)
	overview = models.TextField()
	slug = models.SlugField(null=True, blank=True)
	body_text = RichTextUploadingField(null=True)
	time_upload = models.DateTimeField(auto_now_add = True)
	auther = models.ForeignKey(Author, on_delete=models.CASCADE)
	thumbnail = models.ImageField(upload_to = 'thumbnails')
	publish = models.BooleanField()
	read = models.IntegerField(default = 0)

	class Meta:
		ordering = ['-pk']

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()

class SubComment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

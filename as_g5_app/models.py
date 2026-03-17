from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class userData(models.Model):
  user =  models.OneToOneField(User,on_delete=models.CASCADE)

  #additional field i want to add 
  city=models.CharField(max_length=10)
  zip_code=models.IntegerField()
  state=models.CharField(max_length=10)
  profile_pic=models.ImageField(upload_to='mediaimg/',null=True,blank=True)
  phone_no = models.IntegerField(null=True, blank=True)
  gender=models.CharField(max_length=10,null=True,blank=True)
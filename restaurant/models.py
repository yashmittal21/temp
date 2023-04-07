from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from accounts.models import *

# Create your models here.


class Dish(models.Model):
  owner=ForeignKey(Owner,on_delete = models.CASCADE)
  name=models.CharField(max_length=20)
  price=models.IntegerField()
  #image=models.ImageField()

  def __str__(self):
    return self.name

class Resturant(models.Model):
  owner=ForeignKey(Owner,on_delete = models.CASCADE)
  name=models.CharField(max_length=20)
  address=models.CharField(max_length=200)
  latitude=models.FloatField()
  longitude=models.FloatField()
  opening_time=models.TimeField()
  closing_time=models.TimeField()
  bill_limit=models.IntegerField()
  #rating=models.FloatField()
  #menu:-list of all avalible dish
  #order_list:-
 
  def __str__(self):
    return self.name




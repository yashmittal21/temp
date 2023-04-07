from django.db import models

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length = 20)
	password = models.CharField(max_length = 100)
	location = models.TextField(null = False)
	is_login = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class Owner(models.Model):
	name = models.CharField(max_length = 20)
	password = models.CharField(max_length = 100)
	restaurant_name = models.CharField(max_length = 100)
	is_login = models.BooleanField(default = False)

	def __str__(self):
		return self.name
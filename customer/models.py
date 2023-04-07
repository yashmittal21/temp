from django.db import models
from accounts.models import *
from restaurant.models import *
# Create your models here.
 
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	restaurant_id = models.IntegerField(default = 1)
	status = models.CharField(max_length=100,null = True)
	complete  = models.BooleanField(default = False)

	@property
	def get_cart_total(self):
		orderdish = self.orderdish_set.all()
		sum=0
		for item in orderdish:
			sum = sum + item.get_total
		return sum

	@property
	def get_cart_items(self):
		orderdish = self.orderdish_set.all()
		sum=0
		for item in orderdish:
			sum = sum + item.quantity
		return sum

class Orderdish(models.Model):
	order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(default = 0)
	dish = models.ForeignKey(Dish,on_delete=models.SET_NULL, null=True, blank=True)

	@property
	def get_total(self):
		total = self.dish.price * self.quantity
		return total
import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from accounts.models import *
from restaurant.models import *
from .models import *
from json import dumps
from django.core import serializers

def index(request):
	return render(request,'index.html')
def home(request,id):
	customer = Customer.objects.get(id=id)
	# print(customer.id) 

	request.session["cust_id"] = id
	# if customer.is_login:
	#message=None


	restaurant = Resturant.objects.all()
	data=serializers.serialize("json",restaurant)
	data = dumps(data)
	return render(request,'home.html',{'restaurant' : restaurant,'customer' : customer,'data':data})

def menu(request):
	if request.method == 'POST':
		rest_id = request.POST.get('try')
		request.session["rest_id"]=rest_id
		print(rest_id)
		cust_id = request.session["cust_id"]
		print(cust_id)
		restaurant = Resturant.objects.get(id =rest_id)
		dish = Dish.objects.filter(owner = restaurant.owner)
		if Customer.objects.filter(id = cust_id).exists():
			customer = Customer.objects.get(id = cust_id)
			if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
				order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

			else:
				order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False,status="placed")
				order.save()
				print(order)

			return render(request,'menu.html',{'dish' : dish,'customer' : customer, 'rest_id' : rest_id, 'order' : order})
		else:
			customer = None
			return render(request,'menu.html',{'dish' : dish,'customer' : customer, 'rest_id' : rest_id})
	

def add(request):
	if request.method == 'POST':	
		dish_id = request.POST.get('try')
		dish = Dish.objecst.get(id = dish_id)
		cust_id = request.session["cust_id"]
		customer = Customer.objects.get(id = cust_id)
		if customer.is_login == False :
			return render(request,'customer_login.html')
		owner = dish.owner
		restaurant = Resturant.objects.get(owner = owner)

		if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
			order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

		else:
			order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False,status="placed")
			order.save()
			print(order)

		if Orderdish.objects.filter(order = order,dish = dish).exists():
			orderdish = Orderdish.objects.get(order = order,dish = dish)
			orderdish.quantity = (orderdish.quantity + 1)
			orderdish.save()

		else:
			orderdish = Orderdish.objects.create(order = order,dish = dish,quantity = 1)
			orderdish.save()
		alldish = Dish.objects.filter(owner = owner)
		return render(request,'menu.html',{'dish' : alldish,'customer' : customer, 'order' : order, 'rest_id' : restaurant.id})
	else:
		return redirect('customer_login')


def cart(request):
	cust_id = request.session["cust_id"]
	customer = Customer.objects.get(id = cust_id)
	#rest_id = request.POST.get('restid')
	rest_id = request.session["rest_id"]
	restaurant = Resturant.objects.get(id = rest_id)

	if Order.objects.filter(customer = customer,restaurant_id = restaurant.id, complete = False).exists():
			order = Order.objects.get(customer = customer,restaurant_id = restaurant.id, complete = False)

	else:
		order = Order.objects.create(customer = customer,restaurant_id = restaurant.id, complete = False,status="placed")
		order.save()
		print(order)

	request.session["order_id"]=order.id



	items = Orderdish.objects.filter(order = order).all()
	
	itemsSerializer=serializers.serialize("json",items)
	itemsJSON = dumps(itemsSerializer)## for acessing data in js we need do send data in jsonformat
	context = {'items':items,'order':order,'itemsJSON':itemsJSON,'restaurant':restaurant}
	return render(request,'cart.html',context)




def place_order(request):
	Orderdishes = json.loads(request.POST['data'])##this convert json string into python data structure
	print(Orderdishes)

	for dish in Orderdishes:
		id=dish['id']
		quantity=dish['quantity']
		Orderdish.objects.filter(id=id).update(
			quantity=quantity
		)

	return JsonResponse({"updated succesfully":"ok"})

	



def cart_order(request):
	order_id=request.session.get("order_id")
	print("order_id",order_id)
	Order.objects.filter(id=order_id).update(complete=True)
	cust_id=request.session.get("cust_id")
	#messages.info(request,'Ordered succesfully')

	customer = Customer.objects.get(id=cust_id)
	restaurant = Resturant.objects.all()
	data=serializers.serialize("json",restaurant)
	data = dumps(data)
	return render(request,'home.html',{'restaurant' : restaurant,'customer' : customer,'data':data})

def RemoveOrderDish(request):
	id = json.loads(request.POST['id'])
	instance=Orderdish.objects.get(id=id)

	instance.delete()

	return JsonResponse({'message':'remove'})


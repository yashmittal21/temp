from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
def customer_login(request):
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']

		if Customer.objects.filter(name=name,password=password).exists():
			customer = Customer.objects.get(name=name,password=password)
			# customer.is_login = True
			# customer.save
			Customer.objects.filter(name=name,password=password).update(is_login = True)
			print('customer logged in!!')
			print(customer.is_login)
			return redirect('home',id = customer.id)

		else:
			print('user does not exist')
			messages.warning(request,'invalid credentials')

	return render(request,'customer_login.html')

def customer_signup(request):
	if request.method == 'POST':
		name = request.POST['username']
		p1 = request.POST['password1']
		p2 = request.POST['password2']

		if(p1==p2):
			if Customer.objects.filter(name=name).exists():
				messages.info(request,'username aleady taken')
			else:
				customer = Customer.objects.create(name=name,password=p1)
				customer.save
				print('customer registered')
				return redirect('/')
		else:
			messages.info(request,'password does not matched')
	return render(request,'customer_signup.html')

def owner_login(request):
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']

		if Owner.objects.filter(name=name,password=password).exists():
			owner = Owner.objects.get(name=name,password=password)
			# employee.is_login = True
			# employee.save
			Owner.objects.filter(name=name,password=password).update(is_login = True)
			print('Employee logged in!!')
			return redirect('dashboard',id = owner.id)

		else:
			messages.warning(request,'invalid credentials')

	return render(request,'employee_login.html')

def customer_logout(request):
	if request.method == 'POST':
		cust_id = request.POST.get('try')
		Customer.objects.filter(id = cust_id).update(is_login = False)
		return redirect('home',id=cust_id)
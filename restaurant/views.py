from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from accounts.models import *
from customer.models import Order,Orderdish

# Create your views here.


def dashboard(request,id):
  request.session["owner_id"]=id
  owner=Owner.objects.get(id=id)
  resturant=None
  dishes=None
  order=False
  recieved_order=None
  panding_order=None
  if Resturant.objects.all().filter(owner=owner):
    resturant=Resturant.objects.get(owner=owner)

  if Dish.objects.all().filter(owner=owner):
    dishes=Dish.objects.all().filter(owner=owner)

  if resturant:
    orders_list=Order.objects.filter(restaurant_id=resturant.id,complete=True)
    recieved_order=[]
    panding_order=[]
    # print(orders_list)
    for order in orders_list:
      dishess=Orderdish.objects.filter(order=order)
      # print(dishess)
      if dishess:
        d=[]
        total_bill=0
        for dish in dishess:
          quantity=dish.quantity
          name=dish.dish.name
          price=dish.dish.price
          obj=Info1(name,price,quantity)
          d.append(obj)
          total_bill=total_bill+quantity*price

        obj=Info2(d,order.id,total_bill)

        if order.status=="placed":
          recieved_order.append(obj)
        
        elif order.status=="panding":
          panding_order.append(obj)
    # print(recieved_order)
    # print(panding_order)
    


  if recieved_order or panding_order:
    order=True

  
  return render(request,'dashboard.html',{
    'name':owner.name,
    'id':id,
    'resturant':resturant,
    'dishes':dishes,
    'recieved_order':recieved_order,
    'panding_order':panding_order,
    'order':order
    })

  
def add_resturant(request,owner_id):
  if request.method=="POST":
    owner=Owner.objects.get(id=owner_id)
    name=request.POST["name"]
    address=request.POST["address"]
    latitude=request.POST["latitude"]
    longitude=request.POST["longitude"]
    opening_time=request.POST["opening_time"]
    closing_time=request.POST["closing_time"]
    bill_limit=request.POST["bill_limit"]

    Resturant.objects.create(
      owner=owner,
      name=name,
      address=address,
      latitude=latitude,
      longitude=longitude,
      opening_time=opening_time,
      closing_time=closing_time,
      bill_limit=bill_limit
    )

    return redirect("dashboard",id=owner_id)

  return render(request,'add_resturant.html')


def resturant_details(request,id):
  owner=Owner.objects.get(id=id)
  resturant=Resturant.objects.get(id=id)
  if request.method=="POST":
    name=request.POST["name"]
    address=request.POST["address"]
    latitude=request.POST["latitude"]
    longitude=request.POST["longitude"]
    opening_time=request.POST["opening_time"]
    closing_time=request.POST["closing_time"]
    bill_limit=request.POST["bill_limit"]

    print(latitude)
    print(longitude)

    Resturant.objects.all().filter(owner=owner).update(
      owner=owner,
      name=name,
      address=address,
      latitude=latitude,
      longitude=longitude,
      opening_time=opening_time,
      closing_time=closing_time,
      bill_limit=bill_limit
      )
    return redirect("dashboard",id=id)

  return render(request,'resturant_details.html',{
    'resturant':resturant
  })

def add_dish(request,owner_id):
  owner=Owner.objects.get(id=owner_id)

  if request.method=="POST":
    name=request.POST["name"]
    price=request.POST["price"]

    Dish.objects.create(
      owner=owner,
      name=name,
      price=price
    )
    owner_id=request.session["owner_id"]
    return redirect("dashboard",id=owner_id)


  return render(request,'add_dish.html')

def edit_dish(request,dish_id):
  if request.method=="POST":
    name=request.POST["name"]
    price=request.POST["price"]

    Dish.objects.all().filter(id=dish_id).update(
      name=name,
      price=price
    )

    owner_id=request.session["owner_id"]
    return redirect("dashboard",id=owner_id)


  dish=Dish.objects.get(id=dish_id)
  return render(request,'edit_dish.html',{
    'dish':dish
  })

def remove_dish(request,dish_id):
  instance=Dish.objects.get(id=dish_id)
  instance.delete()

  owner_id=request.session["owner_id"]
  return redirect("dashboard",id=owner_id)

class Info1:
  def __init__(self,name,price,quantity):
    self.name=name
    self.price=price
    self.quantity=quantity

class Info2:
  def __init__(self,dishes,id,bill):
    self.dishes=dishes
    self.id=id
    self.bill=bill




def accept_order(request,order_id):
  Order.objects.filter(id=order_id).update(
    status="panding"
  )

  owner_id=request.session["owner_id"]

  return redirect("dashboard",owner_id)


def reject_order(request,order_id):
  Order.objects.filter(id=order_id).update(
    status="rejected"
  )

  owner_id=request.session["owner_id"]

  return redirect("dashboard",owner_id)


def complete_order(request,order_id):
  Order.objects.filter(id=order_id).update(
    status="completed"
  )

  owner_id=request.session["owner_id"]

  return redirect("dashboard",owner_id)



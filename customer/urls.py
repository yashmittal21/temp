from django.urls import path
from . import views

urlpatterns = [ 
  path("",views.index,name = 'index'),
  path('<int:id>',views.home,name = 'home'),
  path('menu/',views.menu,name = 'menu'),
  path('add/',views.add,name='add'),
  path('cart/',views.cart,name='cart'),
  path('place_order',views.place_order,name="place_order"),
  path('cart_order/',views.cart_order,name="cart_order"),
  path('remove_order_dish',views.RemoveOrderDish,name="remove_order_dish")
]

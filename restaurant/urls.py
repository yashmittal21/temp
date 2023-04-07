from django.urls import path
from . import views

urlpatterns = [
  path('dashboard/<int:id>',views.dashboard,name="dashboard"),
  path('dashboard/add_resturant/<int:owner_id>',views.add_resturant,name="add_resturant"),
  path('dashboard/resturant_details/<int:id>',views.resturant_details,name="resturant_details"),
  path('dashboard/add_dish/<int:owner_id>',views.add_dish,name="add_dish"),
  path('dashboard/edit_dish/<int:dish_id>',views.edit_dish,name="edit_dish"),
  path('dashboard/remove_dish/<int:dish_id>',views.remove_dish,name="remove_dish"),
  path('dashboard/accept_order/<int:order_id>',views.accept_order,name="accept_order"),
  path('dashboard/reject_order/<int:order_id>',views.reject_order,name="reject_order"),
  path('dashboard/complete_order/<int:order_id>',views.complete_order,name="complete_order")



]
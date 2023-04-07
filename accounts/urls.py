from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path("customer_login",views.customer_login,name = 'customer_login'),
	path("customer_signup/",views.customer_signup,name = 'customer_signup'),
	path("owner_login/",views.owner_login,name = 'owner_login'),
	path("customer_logout",views.customer_logout,name = 'customer_logout'),
]
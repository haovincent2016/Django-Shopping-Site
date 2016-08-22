from django.conf.urls import url
from rest_framework.generics import ListAPIView
from .serializers import ShoppingSerializer
from .models import CartItem
from . import views
from .views import CartList

urlpatterns = [
	url(r'^product/add/$', views.add_product, name='add'),
	url(r'^product/edit/(?P<id>[^/]+)/$', views.edit_product, name='edit'),
	url(r'^product/view/(?P<id>[^/]+)/$', views.view_product, name='view'),
	url(r'^product/delete/(?P<id>[^/]+)/$', views.delete_product, name='delete'),
	url(r'^product/list/$', views.product_list, name='list'),
	#catalog page for users/buyers
	url(r'^catalog/$', views.catalog, name='catalog'),
	#cart page for users/buyers
	url(r'^cart/$', views.view_cart),
	#add to cart
	url(r'^cart/add/(?P<id>[^/]+)/$', views.add_to_cart, name='addcart'),
	#clear cart
	url(r'^cart/clear/$', views.clear_cart, name='clearcart'),
	#rest api
	url(r'^restapi/$', CartList.as_view()),
	#create order
	url(r'^order/$', views.create_order),
	#view order
	url(r'^order/view/$', views.view_order),
	#delete order
	url(r'^order/delete/(?P<id>[^/]+)$', views.delete_order),
]
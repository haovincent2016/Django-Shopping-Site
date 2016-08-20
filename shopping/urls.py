from django.conf.urls import url
from rest_framework.generics import ListCreateAPIView
from .serializers import ShoppingSerializer
from .models import CartItem
from . import views

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
	url(r'^restapi/$', ListCreateAPIView.as_view(queryset=CartItem.objects.all(), serializer_class=ShoppingSerializer)),
]
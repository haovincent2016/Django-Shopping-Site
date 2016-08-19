from django.conf.urls import url
from . import views

app_name = 'shopping'
urlpatterns = [
	url(r'^product/add/$', views.add_product),
	url(r'^product/edit/(?P[0-9]+)/$', views.edit_product),
	url(r'^product/view/(?P[0-9]+)/($', views.view_product),
	url(r'^product/delete/$', views.delete_product),
	url(r'^product/list/$', views.product_list),
]
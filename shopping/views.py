from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from . import forms
from . import models
#add
def add_product(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = ProductForm()
	template = loader.get_template('shopping/add-product.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))
#edit
def edit_product(request, id):
	product = Product.objects.get(id=id)
	form = ProductForm(request.POST or None, instance = product_instance)
	if form.is_valid():
		form.save()
	template = loader('shopping/edit_product.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))
#view
def view_product(request, id):
    product_instance = Product.objects.get(id = id)
	template = loader('shopping/view_product.html')
    context = {'product_instance':  product_instance}
    return HttpResponse(template.render(context, request))
#list
def product_list(request):
	product_list = Product.objects.all()
	#show 15 items per page
    paginator = Paginator(product_list ,15)
	page = request.GET.get('page')
	#return specific page content or first page(NAI) or last page(OOR)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	template = loader('shopping/product_list.html')
    context = {'products': products)
    return HttpResponse(template.render(context, request))
#delete

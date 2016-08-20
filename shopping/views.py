from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .forms import ProductForm, DeleteForm
from .models import Product, CartItem, Cart
#add
def add_product(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = ProductForm()
		#return to the list page
		return HttpResponseRedirect(reverse('list'))
	template = loader.get_template('shopping/add_product.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))
#edit
def edit_product(request, id):
	product = Product.objects.get(id=id)
	form = ProductForm(request.POST or None, instance = product)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('list'))
	template = loader.get_template('shopping/edit_product.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))
#view
def view_product(request, id):
	product_instance = Product.objects.get(id = id)
	template = loader.get_template('shopping/view_product.html')
	context = {'product_instance':  product_instance}
	return HttpResponse(template.render(context, request))
#list
def product_list(request):
	product_list = Product.objects.all()
	#show 15 items per page
	paginator = Paginator(product_list, 15)
	page = request.GET.get('page')
	#return specific page content or first page(NAI) or last page(OOR)
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	template = loader.get_template('shopping/product_list.html')
	context = {'products': products}
	return HttpResponse(template.render(context, request))
#delete
def delete_product(request, id):
	product = get_object_or_404(Product, id=id)
	if request.method == 'POST':
		form = DeleteForm(request.POST, instance=product)
		if form.is_valid():
			product.delete()
			return HttpResponseRedirect(reverse('list'))
	else:
		form = DeleteForm(instance=product)
	template = loader.get_template('shopping/delete_product.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))
	
#catalog view(for buyer)
def catalog(request):
	cart = request.session.get("cart",None)
	products = Product.objects.filter(release_date__lt = timezone.now().date()).order_by("-release_date")
	template = loader.get_template('shopping/catalog.html')
	context = {'products': products, 'cart': cart}
	return HttpResponse(template.render(context, request))

#cart view(for buyer)
def view_cart(request):
	cart = request.session.get("cart", None)
	template = loader.get_template('shopping/view_cart.html')
	if not cart:
		cart = Cart()
	request.session['cart'] = cart
	context = {'cart': cart}
	return HttpResponse(template.render(context, request))
#add to cart
def add_to_cart(request,id):
	product = Product.objects.get(id = id)
	cart = request.session.get("cart",None)
	if not cart:
		cart = Cart()
	request.session["cart"] = cart
	cart.add_product(product)
	request.session['cart'] = cart
	return view_cart(request)
#clear cart
def clear_cart(request):
	request.session['cart'] = Cart()
	return view_cart(request)

# #Rest api
# def post(self, request, *args, **kwargs):
	# print request.POST['product']
	# product = Product.objects.get(id=request.POST['product'])
	# cart = request.session['cart']
	# cart.add_product(product)
	# request.session['cart'] = cart
	# return request.session['cart'].items

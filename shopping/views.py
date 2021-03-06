from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ShoppingSerializer
from rest_framework.renderers import JSONRenderer

from .forms import ProductForm, OrderForm, DeleteForm
from .models import Product, CartItem, Cart, Order

# class JSONResponse(HttpResponse):
	# def __init__(self, data, **kwargs):
		# content = JSONRenderer().render(data)
		# kwargs['content_type'] = 'application/json'
		# super(JSONResponse, self).__init__(content, **kwargs)

class CartList(APIView):
	def get(self, request, *args, **kwargs):
		#return request.session['cart'].items
		cartitems = CartItem.objects.all()
		serializer = ShoppingSerializer(cartitems, many=True)
		return Response(serializer.data)
	def post(self, request, *args, **kwargs):
		#id is from post request key product value
		product = Product.objects.get(id=request.POST['product'])
		cart = request.session['cart']
		cart.add_product(product)
		#update cart session
		request.session['cart'] = cart
		return request.session['cart'].items
		
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
#list (require login to access)
@login_required
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
	return catalog(request)

#create order
def create_order(request):
	form = OrderForm(request.POST or None)
	if form.is_valid():
		order = form.save()
		for item in request.session['cart'].items:
			item.order = order
			item.save()
		clear_cart(request)
		return HttpResponseRedirect(reverse('catalog'))
	template = loader.get_template('shopping/create_order.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))

#view all orders
def view_order(request):
	order_list = Order.objects.all()
	#show 15 items per page
	paginator = Paginator(order_list, 15)
	page = request.GET.get('page')
	#return specific page content or first page(NAI) or last page(OOR)
	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages)
	template = loader.get_template('shopping/view_order.html')
	context = {'orders': orders}
	return HttpResponse(template.render(context, request))
#delete specific order history
def delete_order(request, id):
	order = get_object_or_404(Order, id=id)
	if request.method == 'POST':
		form = DeleteForm(request.POST, instance=order)
		if form.is_valid():
			order.delete()
			return HttpResponseRedirect(reverse('catalog'))
	else:
		form = DeleteForm(instance=order)
	template = loader.get_template('shopping/delete_order.html')
	context = {'form': form}
	return HttpResponse(template.render(context, request))

#login
def login_view(request):
	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
		login(request, user)
		print(request.user)
		return product_list(request)
	else:
		return catalog(request)
#logout
def logout_view(request):
	logout(request)
	return catalog(request)
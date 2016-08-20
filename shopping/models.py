from django.db import models
import json

class Product(models.Model):
	#id = models.AutoField(primary_key=True) is given by default
	name = models.CharField(max_length=100, unique=True)
	image = models.URLField(max_length=200)
	description = models.TextField()
	release_date = models.DateField()
	price = models.DecimalField(max_digits=9, decimal_places=2)
	free_shipping = models.BooleanField()

class Order(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	address = models.TextField()
	payment = models.CharField(max_length=50)

class CartItem(models.Model):
	product = models.ForeignKey(Product)
	order = models.ForeignKey(Order, null=True)
	item_price = models.DecimalField(max_digits=9, decimal_places=2)
	quantity = models.IntegerField()

class Cart(object):
	def __init__(self):
		self.items = []
		self.total_price = 0
	def add_product(self, product):
		self.total_price += product.price
		for item in self.items:
			if item.product.id == product.id:
				item.quantity += 1
				return
		return self.items.append(CartItem(product=product, item_price=product.price, quantity=1))

 
	
    
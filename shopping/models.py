from django.db import models

class Product(models.Model):
	#id = models.AutoField(primary_key=True) is given by default
	name = models.CharField(max_length=100)
	image = models.CharField(max_length=200)
	description = models.TextField()
	release_data = models.DateField()
	price = models.DecimalField(max_digits=9, decimal_places=2)
	free_shipping = models.BooleanField()
	
    
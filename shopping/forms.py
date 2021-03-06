from django.forms import ModelForm
from .models import Product, Order

def anyTrue(predicate, sequence):
	return True in list(map(predicate, sequence))
def endsWith(s, *endings):
	return anyTrue(s.endswith, endings)

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
	def clean_price(self):
		price = self.cleaned_data['price']
		if price <= 0:
			raise forms.ValidationError("invalid price")
		return price
	def clean_image(self):
		url = self.cleaned_data['image']
		if not endsWith(url.lower(), ('.jpg', '.png', '.gif')):
			raise forms.ValidationError('image must be in the format of jpg, png or gif')
		return url
		
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
	def clean_payment(self):
		payment = self.cleaned_data['payment']
		if not endsWith(payment.lower(), ('credit card', 'master card', 'debit card')):
			raise forms.ValidationError('we only accept credit card, master card or debit card')
		return payment

class DeleteForm(ModelForm):
	class Meta:
		model = Product
		fields = []
	
    
	# def __init__(self, *args, **kwargs):
        # super(ProductForm, self).__init__(*args, **kwargs)
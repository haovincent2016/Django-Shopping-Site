from django.forms import ModelForm
from .models import Product

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

class DeleteForm(ModelForm):
	class Meta:
		model = Product
		fields = []
	
    
	# def __init__(self, *args, **kwargs):
        # super(ProductForm, self).__init__(*args, **kwargs)
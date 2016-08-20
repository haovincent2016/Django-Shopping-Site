from .models import CartItem
from rest_framework import serializers

class ShoppingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartItem
		fields = '__all__'
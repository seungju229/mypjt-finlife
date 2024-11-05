from rest_framework import serializers
from .models import DepositProducts, DepositOptions


class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class ProductOptionSerializer(serializers.ModelSerializer):
    class OptionSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = '__all__'
    
    depositoptions_set = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProducts
        fields = '__all__'
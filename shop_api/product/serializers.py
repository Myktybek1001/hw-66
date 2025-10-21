from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = 'id name product_count'.split()

    def get_product_count (self, obj):
        return obj.product_set.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category reviews '.split()




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


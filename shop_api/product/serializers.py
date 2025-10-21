from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()


    class Meta:
        model = Category
        fields = 'id name product_count'.split()

    def get_product_count (self, obj):
        return obj.product_set.count()

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category reviews '.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=5, max_length=300)
    stars = serializers.IntegerField()
    product = serializers.IntegerField()

    def validate_stars(self, value):
        if not (1 <= value <= 5):
            raise ValidationError("1 to 5 stars ")
        return value

    def validate_product(self, value):
        if not Product.objects.filter(id=value).exists():
            raise ValidationError("Product not found")
        return value

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100,min_length=1, )
    description = serializers.CharField(min_length=1, max_length=250)
    price = serializers.FloatField()
    category = serializers.IntegerField()

    def validate_category(self, value):
        try:
            Category.objects.get(pk=value)
        except Category.DoesNotExist:
            raise ValidationError('Category not found')
        return value




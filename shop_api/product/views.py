from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer,ProductValidateSerializer
from django.db import transaction


# product
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product not found'}, status=404)

    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category')
        product.save()

        return Response(status=status.HTTP_200_OK,
                        data=ProductSerializer(product).data)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':

        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)
        
        #1
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category')

        #2
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category_id=category_id
            )
        #3
        return Response(status=status.HTTP_201_CREATED,
                         data=ProductSerializer(product).data)


# categor

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(name=serializer.validated_data.get('name'))
        return Response(data=CategorySerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(data={'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(data=CategorySerializer(category).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# review


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            text=serializer.validated_data.get('text'),
            stars=serializer.validated_data.get('stars'),
            product_id=serializer.validated_data.get('product')
        )
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(data={'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product')
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
   


class CategoryDetail(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer





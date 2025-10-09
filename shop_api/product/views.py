from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


@api_view(['GET'])
def product_detail_api_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        data = ProductSerializer(product).data
        return Response(data=data)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product not found'}, status=404)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data)


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





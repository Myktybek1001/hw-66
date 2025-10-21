from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category')
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
        
        #1
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category')

        #2
        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
            
        )
        

        #3
        return Response(status=status.HTTP_201_CREATED,
                         data=ProductSerializer(product).data)


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
   


class CategoryDetail(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer





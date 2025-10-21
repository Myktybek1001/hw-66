from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



STARS = [(i, '*' * i) for i in range(1, 6)]

class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
   
    def __str__(self):
        return self.text

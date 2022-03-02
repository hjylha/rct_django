from django.db import models

# Create your models here.




class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    alternative_name = models.CharField(max_length=64, unique=True, null=True)
    cost = models.IntegerField()
    price_base = models.IntegerField()
    price_hot = models.IntegerField()
    price_cold = models.IntegerField()
    price_initial = models.IntegerField()
    buy_during_rain = models.BooleanField()

    def __str__(self) -> str:
        return str(self.name)


class Stall(models.Model):
    name = models.CharField(max_length=64, unique=True)
    cost = models.IntegerField()
    # each stall can only sell two products?
    products = models.ManyToManyField(Product)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product2 = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return str(self.name)

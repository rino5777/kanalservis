from django.db import models

# Create your models here.
class Data_google(models.Model):


    num = models.CharField(max_length = 50, null=True, blank=True, unique=False)
    order  = models.CharField(max_length = 50, null=True, blank=True)
    priceUSD  = models.CharField(max_length = 50, null=True, blank=True, unique=False)
    date_arr = models.CharField(max_length = 50, null=True, blank=True, unique=False)
    priceRUB  = models.CharField(max_length = 50, null=True, blank=True, unique=False)
    actual = models.BooleanField(default=True)

    def __str__(self):
            return str(self.order)
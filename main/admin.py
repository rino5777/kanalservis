from django.contrib import admin
from .models import Data_google
# Register your models here.




@admin.register(Data_google)
class Data_googleAdmin(admin.ModelAdmin):
    list_display = ('num', 'order', 'priceUSD', 'date_arr', 'priceRUB')
from django.contrib import admin
from .models import Inventory,InventoryGroup, Shop
# Register your models here.

admin.site.register((InventoryGroup,Inventory,Shop),)
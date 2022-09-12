from django.contrib import admin
from . models import *

# Register your models here.
class Product_Images_Admin(admin.TabularInline):
    model = Product_Image

class Additional_Informations_Admin(admin.TabularInline):
    model = Additional_information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images_Admin, Additional_Informations_Admin)
    list_display = ('name', 'price', 'categories', 'color', 'section')
    list_editable = ('categories', 'color', 'section')

admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_information)
admin.site.register(Brand)
admin.site.register(Slider)
admin.site.register(Banner)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Color)

admin.site.register(Coupon_Code)
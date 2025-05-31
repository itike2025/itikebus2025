from django.contrib import admin
from .models import  Order, CartItem, LineItem, Like, Slider

# Register your models here.

# Register your models here.

#class TagAdmin(admin.ModelAdmin):
    #list_display = ('first_name', 'last_name')
    #pass






#class ProductAdmin(admin.ModelAdmin):
    #list_display =['id', 'name', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'date', 'paid']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'bus']


class LineItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'order']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user','bus','value')


#admin.site.register(Product, ProductAdmin)
#admin.site.register(Tag, TagAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem, OrderItemAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Slider)

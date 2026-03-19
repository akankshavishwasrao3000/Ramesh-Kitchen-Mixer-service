from django.contrib import admin
from ramesh.models import Repair 
from ramesh.models import Order

class RepairAdmin(admin.ModelAdmin):
   list_display=('name','email','mobile','city','description','created_at')

admin.site.register(Repair, RepairAdmin)
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
      list_display = ( 'product_name', 'name', 'phone', 'address', 'price', 'quantity', 'total', 'created_at')


admin.site.register(Order, OrderAdmin)



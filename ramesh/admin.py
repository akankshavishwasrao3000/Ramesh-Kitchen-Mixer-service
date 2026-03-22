from django.contrib import admin
from ramesh.models import Repair 
from ramesh.models import Order
from ramesh.models import Profile

class RepairAdmin(admin.ModelAdmin):
   list_display=('name','email','mobile','city','description','created_at')

admin.site.register(Repair, RepairAdmin)
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
      list_display = ( 'product_name', 'name', 'phone', 'address', 'price', 'quantity', 'total', 'created_at')
admin.site.register(Order, OrderAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')



# The @ symbol is called a decorator in Python.

# In this case:

# @admin.register(Profile)

# is just a shorter way of writing this:

# admin.site.register(Profile, ProfileAdmin)

# Both do the same thing.
from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from ramesh.models import Repair, Order, Profile, Product
from .forms import OrderAdminForm
from .order_services import (
    OrderInventoryError,
    create_order,
    delete_order,
    update_order,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_available')


class RepairAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'city', 'description', 'created_at')


admin.site.register(Repair, RepairAdmin)


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ('product_name', 'name', 'phone', 'address', 'price', 'quantity', 'total', 'order_status', 'delivery_days', 'created_at')

    readonly_fields = ('product_name', 'price', 'total', 'reserved_quantity', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly_fields.append('product')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            saved_order = create_order(
                product_id=form.cleaned_data['product'].pk,
                user=form.cleaned_data.get('user'),
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                quantity=form.cleaned_data['quantity'],
                order_status=form.cleaned_data['order_status'],
                delivery_days=form.cleaned_data['delivery_days'],
            )
            obj.pk = saved_order.pk
            obj.refresh_from_db()
            return

        updates = {
            field: form.cleaned_data[field]
            for field in ('user', 'name', 'phone', 'address', 'order_status', 'delivery_days')
            if field in form.changed_data
        }
        update_order(obj.pk, quantity=form.cleaned_data['quantity'], updates=updates)
        obj.refresh_from_db()

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super().changeform_view(request, object_id, form_url, extra_context)
        except OrderInventoryError as exc:
            self.message_user(request, str(exc), level=messages.ERROR)
            return redirect('admin:ramesh_order_changelist')

    def delete_model(self, request, obj):
        delete_order(obj.pk)

    def delete_queryset(self, request, queryset):
        with transaction.atomic():
            for order_id in queryset.values_list('pk', flat=True):
                delete_order(order_id)


admin.site.register(Order, OrderAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')

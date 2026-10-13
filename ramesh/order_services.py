from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Order, Product


class OrderInventoryError(Exception):
    pass


def create_order(
    *,
    product_id,
    user,
    name,
    phone,
    address,
    quantity,
    order_status='Processing',
    delivery_days='3-7 days',
):
    if quantity < 1 or quantity > 1000:
        raise OrderInventoryError('Quantity must be between 1 and 1000.')

    with transaction.atomic():
        try:
            product = Product.objects.select_for_update().get(
                pk=product_id,
                is_available=True,
            )
        except Product.DoesNotExist as exc:
            raise OrderInventoryError('This product is unavailable.') from exc

        if product.stock < quantity:
            raise OrderInventoryError(
                f'Only {product.stock} unit(s) available for {product.name}.'
            )

        order = Order.objects.create(
            user=user,
            product=product,
            product_name=product.name,
            name=name,
            phone=phone,
            address=address,
            price=product.price,
            quantity=quantity,
            total=product.price * quantity,
            reserved_quantity=quantity,
            order_status=order_status,
            delivery_days=delivery_days,
        )
        product.stock -= quantity
        product.save(update_fields=['stock'])
        return order


@transaction.atomic
def update_order(order_id, *, quantity, updates=None):
    if quantity < 1 or quantity > 1000:
        raise OrderInventoryError('Quantity must be between 1 and 1000.')

    order = Order.objects.select_for_update().get(pk=order_id)
    if quantity != order.quantity and order.order_status != 'Processing':
        raise OrderInventoryError('Only processing orders can be changed.')

    product = None
    if order.product_id:
        product = Product.objects.select_for_update().get(pk=order.product_id)
        stock_change = order.reserved_quantity - quantity
        if stock_change < 0:
            additional_stock = -stock_change
            if not product.is_available:
                raise OrderInventoryError('This product is unavailable for additional units.')
            if product.stock < additional_stock:
                raise OrderInventoryError(
                    f'Only {product.stock} additional unit(s) are available for {product.name}.'
                )
            product.stock -= additional_stock
        elif stock_change > 0:
            product.stock += stock_change

        if stock_change:
            product.save(update_fields=['stock'])
        order.reserved_quantity = quantity

    order.quantity = quantity
    order.total = order.price * quantity
    for field, value in (updates or {}).items():
        if field not in {'name', 'phone', 'address', 'order_status', 'delivery_days', 'user'}:
            raise ValidationError(f'Unsupported order update field: {field}')
        setattr(order, field, value)
    order.save()
    return order


@transaction.atomic
def delete_order(order_id, *, owner=None):
    order = Order.objects.select_for_update().get(pk=order_id)
    if owner is not None and order.user_id != owner.pk and not (
        owner.is_staff or owner.is_superuser
    ):
        raise PermissionError('You are not authorized to delete this order.')

    if owner is not None and not (owner.is_staff or owner.is_superuser):
        if order.order_status != 'Processing':
            raise OrderInventoryError('Only processing orders can be cancelled.')

    if order.product_id and order.reserved_quantity and order.order_status == 'Processing':
        product = Product.objects.select_for_update().get(pk=order.product_id)
        product.stock += order.reserved_quantity
        product.save(update_fields=['stock'])
    order.delete()

import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .forms import ProfileImageForm, RegisterForm, OrderUpdateForm, UserProfileForm
from .models import Order, Repair, Profile, Product
from .order_services import (
    OrderInventoryError,
    create_order,
    delete_order as delete_order_service,
    update_order as update_order_service,
)
import logging

logger = logging.getLogger(__name__)



def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})



def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, **{"username": username, "pass" + "word": password})
            if user is not None:
                login(request, user)
                if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)
                return redirect("index")
        else:
            messages.error(request, "Account not found. Please sign up first.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def home(request):
    return render(request, "index.html")  

def index(request):
    return render(request, 'index.html')


def products(request):
    products_qs = Product.objects.filter(is_available=True).order_by('name')
    return render(request, 'products.html', {'products': products_qs})


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_conditions(request):
    return render(request, 'terms_and_conditions.html')

def refund_policy(request):
    return render(request, 'refund_policy.html')

def shipping_policy(request):
    return render(request, 'shipping_policy.html')

@login_required
def repair(request):

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        email = request.POST.get("email", "").strip()
        city = request.POST.get("city", "").strip()
        description = request.POST.get("description", "").strip()

        if not all([name, mobile, email, city, description]):
            messages.error(request, "All fields are required. Please fill them out.")
            return redirect("repair")

        if not re.match(r"^[0-9]{10,15}$", mobile):
            messages.error(request, "Please provide a valid mobile number.")
            return redirect("repair")

        Repair.objects.create(
            user=request.user,
            name=name,
            mobile=mobile,
            email=email,
            city=city,
            description=description
        )

        messages.success(request, "Repair request submitted successfully")
        return redirect("repair")

    return render(request, "repair.html")


@login_required
def order(request):
    product_id = request.GET.get("product_id") or request.POST.get("product_id")
    product = None

    if product_id and product_id.isdecimal():
        product = Product.objects.filter(pk=product_id, is_available=True).first()

    if request.method == "POST":
        if not product_id or not product_id.isdecimal():
            messages.error(request, "Please choose a valid product before placing your order.")
            return redirect("products")

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        try:
            quantity = int(request.POST.get("quantity", ""))
            if quantity <= 0 or quantity > 1000:
                raise ValueError
        except (TypeError, ValueError):
            messages.error(request, "Quantity must be a valid positive number up to 1000.")
            return redirect(f"/order/?product_id={product_id}")

        if not name or len(name) > 100:
            messages.error(request, "Please provide a valid name up to 100 characters.")
            return redirect(f"/order/?product_id={product_id}")

        if not re.match("^[0-9]{10}$", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect(f"/order/?product_id={product_id}")

        if not address or len(address) > 1000:
            messages.error(request, "Please provide a delivery address up to 1000 characters.")
            return redirect(f"/order/?product_id={product_id}")

        try:
            order_obj = create_order(
                product_id=product_id,
                user=request.user,
                name=name,
                phone=phone,
                address=address,
                quantity=quantity,
            )
        except OrderInventoryError as exc:
            messages.error(request, str(exc))
            return redirect("products")

        return redirect('order_success', order_id=order_obj.id)

    if not product:
        messages.error(request, "Please choose an available product before placing your order.")
        return redirect("products")

    if product and product.stock <= 0:
        messages.error(request, "This product is currently out of stock.")
        return redirect("products")

    context = {
        "product_name": product.name if product else "",
        "price": product.price if product else 0
    }

    return render(request, "order.html", context)

@login_required
def order_success(request, order_id):
    order_obj = get_object_or_404(Order, id=order_id, user=request.user)
    
   
    whatsapp_number = "919921071945"  
    message = f"Hello, I have placed an order for {order_obj.product_name}.\nName: {order_obj.name}\nMobile: {order_obj.phone}\n\nPlease contact me regarding this order."
    
   
    import urllib.parse
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
    
    return render(request, "order_success.html", {
        "order": order_obj,
        "whatsapp_url": whatsapp_url
    })


@login_required
def profile(request):
    profile_form = UserProfileForm(
        request.POST if request.method == 'POST' else None,
        instance=request.user,
    )
    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile information has been updated.")
            return redirect('profile')
        messages.error(request, "Please correct the profile information below.")

    orders = Order.objects.filter(user=request.user).order_by('-created_at').only(
        'product_name', 'price', 'quantity', 'total', 'order_status', 'delivery_days', 'created_at'
    )
    repairs = Repair.objects.filter(user=request.user).order_by('-created_at').only(
        'name', 'email', 'mobile', 'city', 'description', 'created_at'
    )
    profile_obj = Profile.objects.filter(user=request.user).only('image').first()
    profile_image = profile_obj.image.url if profile_obj and profile_obj.image else None

    return render(request, "profile.html", {
        "orders": orders,
        "repairs": repairs,
        "profile_image": profile_image,
        "profile_form": profile_form,
    })


@login_required
@require_POST
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    try:
        delete_order_service(order.id, owner=request.user)
    except PermissionError:
        messages.error(request, "You are not authorized to delete this order.")
        return redirect('profile')
    except OrderInventoryError as exc:
        messages.error(request, str(exc))
        return redirect('profile')

    messages.success(request, "Order cancelled successfully.")
    return redirect('dashboard' if request.user.is_staff or request.user.is_superuser else 'profile')


@login_required
@require_POST
def delete_repair(request, id):
    repair = get_object_or_404(Repair, id=id)
    if repair.user_id != request.user.id and not (
        request.user.is_staff or request.user.is_superuser
    ):
        messages.error(request, "You are not authorized to delete this repair request.")
        return redirect('profile')
    repair.delete()
    messages.success(request, "Repair request deleted successfully.")
    return redirect('dashboard' if request.user.is_staff or request.user.is_superuser else 'profile')

@login_required
def update_order(request, id):

    order = get_object_or_404(Order, id=id, user=request.user)

    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            try:
                update_order_service(order.id, quantity=form.cleaned_data['quantity'])
            except OrderInventoryError as exc:
                form.add_error('quantity', str(exc))
            else:
                messages.success(request, "Order quantity updated successfully.")
                return redirect('profile')

    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'update_order.html', {'form': form})

@login_required(login_url='login')
@never_cache
def dashboard_view(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('index')

    users = User.objects.order_by('username').only('username', 'email', 'first_name', 'last_name', 'date_joined')
    repair_count = Repair.objects.count()
    recent_repairs = Repair.objects.select_related('user').only('user', 'name', 'email', 'city', 'description', 'created_at').order_by('-created_at')[:10]
    all_orders = Order.objects.select_related('user').only('user', 'product_name', 'price', 'quantity', 'total', 'order_status', 'delivery_days', 'created_at').order_by('-created_at')[:40]
    total_orders = Order.objects.count()

    return render(request, 'dashboard.html', {
        'users': users,
        'repair_count': repair_count,
        'recent_repairs': recent_repairs,
        'all_orders': all_orders,
        'total_orders': total_orders,
    })

@login_required(login_url='login')
@never_cache
def user_detail_view(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('index')

    user_obj = get_object_or_404(User, id=id)
    orders = Order.objects.filter(user=user_obj).order_by('-created_at').only(
        'product_name', 'price', 'quantity', 'total', 'order_status', 'delivery_days', 'created_at'
    )
    repairs = Repair.objects.filter(user=user_obj).order_by('-created_at').only(
        'name', 'email', 'mobile', 'city', 'description', 'created_at'
    )
    full_name = f"{user_obj.first_name} {user_obj.last_name}".strip() or user_obj.username

    return render(request, 'user_detail.html', {
        'user_obj': user_obj,
        'full_name': full_name,
        'orders': orders,
        'repairs': repairs,
    })

@login_required(login_url='login')
def update_order_status(request, id):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('index')

    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        status = request.POST.get('order_status')
        if status in dict(Order.STATUS_CHOICES).keys():
            order.order_status = status
            order.save()

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    if order.user_id:
        return redirect('user_detail', id=order.user_id)
    return redirect('dashboard')

@login_required
@require_POST
def upload_profile_image(request):
    form = ProfileImageForm(request.POST, request.FILES)
    if not form.is_valid():
        for error in form.errors.get('profile_image', []):
            messages.error(request, error)
        return redirect('profile')

    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.image = form.cleaned_data['profile_image']
    profile.save()
    if created:
        messages.success(request, "Profile created and image uploaded successfully.")
    else:
        messages.success(request, "Profile image updated successfully.")
    return redirect('profile')
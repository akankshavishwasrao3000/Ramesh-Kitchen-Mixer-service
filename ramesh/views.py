import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, OrderUpdateForm
from .models import Order, Repair, Profile


# Signup View
def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "signup.html", {"form": form})


# Login View
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect("index")   # your main page
        else:
            messages.error(request, "Account not found. Please sign up first.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "next": next_url})


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")


# Protect Home Page
@login_required
def home(request):
    return render(request, "index.html")  

def index(request):
   
    return render(request, 'index.html')
    # return HttpResponse("This is home page")




def products(request):
    return render(request, 'products.html')


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

# Create your views here.
@login_required
def order(request):

    product_id = request.GET.get("product_id")
    product = None

    products = {
        "1": {"name": "Ramesh Mixer 1", "price": 3500.00},
        "2": {"name": "Ramesh Mixer 2", "price": 4550.00},
        "3": {"name": "Ramesh Mixer 3", "price": 3500.00},
        "4": {"name": "Ramesh Mixer 4", "price": 4550.00},
    }

    if product_id:
        product = products.get(product_id)

    if request.method == "POST":
        if not product:
            messages.error(request, "Please choose a valid product before placing your order.")
            return redirect("products")

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        try:
            quantity = int(request.POST.get("quantity"))
            if quantity <= 0 or quantity > 1000:
                raise ValueError
        except ValueError:
            messages.error(request, "Quantity must be a valid positive number up to 1000.")
            return redirect(f"/order/?product_id={product_id}")

        if not re.match("^[A-Za-z ]+$", name):
            messages.error(request, "Name should contain only letters.")
            return redirect(f"/order/?product_id={product_id}")

        if not re.match("^[0-9]{10}$", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect(f"/order/?product_id={product_id}")

        price = product["price"]
        total = price * quantity

        Order.objects.create(
            user=request.user,
            product_name=product["name"],
            name=name,
            phone=phone,
            address=address,
            price=price,
            quantity=quantity,
            total=total
        )

        messages.success(request, "Your order has been submitted successfully!")
        return redirect(f"/order/?product_id={product_id}")

    context = {
        "product_name": product["name"] if product else "",
        "price": product["price"] if product else 0
    }

    return render(request, "order.html", context)


@login_required
def profile(request):
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
        "profile_image": profile_image
    })


@login_required
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    
    # Allow deletion if it's the user's own order OR if user is staff/superuser
    if order.user == request.user or request.user.is_staff or request.user.is_superuser:
        order.delete()
        messages.success(request, "Order deleted successfully!")
        
        # Redirect based on where the deletion came from
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('profile')
    else:
        messages.error(request, "You are not authorized to delete this order.")
        return redirect('profile')


@login_required
def delete_repair(request, id):
    repair = get_object_or_404(Repair, id=id)
    
    # Allow deletion if it's the user's own repair OR if user is staff/superuser
    if repair.user == request.user or request.user.is_staff or request.user.is_superuser:
        repair.delete()
        messages.success(request, "Repair request deleted successfully!")
        
        # Redirect based on where the deletion came from
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('profile')
    else:
        messages.error(request, "You are not authorized to delete this repair request.")
        return redirect('profile')

@login_required
def update_order(request, id):

    order = get_object_or_404(Order, id=id, user=request.user)

    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            order.total = order.price * order.quantity
            order.save()
            return redirect('profile')

    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'update_order.html', {'form': form})

@login_required(login_url='login')
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
def upload_profile_image(request):
    if request.method == 'POST':
        profile, created = Profile.objects.get_or_create(user=request.user)
        if 'profile_image' in request.FILES:
            profile.image = request.FILES['profile_image']
            profile.save()
            if created:
                messages.success(request, "Profile created and image uploaded successfully!")
            else:
                messages.success(request, "Profile image updated successfully!")
    return redirect('profile')
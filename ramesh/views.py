import re
from unicodedata import name
from django.shortcuts import render  ,redirect , get_object_or_404
from matplotlib.style import context
from requests import request 
from ramesh.models import Repair
from datetime import datetime
from django.contrib import messages
from ramesh.models import Order
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Repair
from .models import Order, Repair, Profile
from .forms import OrderUpdateForm

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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")   # your main page
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")


# Protect Home Page
@login_required
def home(request):
    return render(request, "index.html")  # your main project page

def index(request):
   
    return render(request, 'index.html')
    # return HttpResponse("This is home page")

def products(request):

    return render(request, 'products.html')

def services(request):
   
   return render(request, 'services.html')

def contact(request):

    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def repair(request):

    if request.method == "POST":

        # ⭐ Check login FIRST
        if not request.user.is_authenticated:
            return redirect("/login/")

        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        city = request.POST.get("city")
        description = request.POST.get("description")

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

    if request.method == "POST" and product:

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        try:
            quantity = int(request.POST.get("quantity"))
            if quantity <= 0:
                raise ValueError
        except:
            messages.error(request, "Quantity must be a valid positive number.")
            return redirect("/order/?product_id=" + product_id)

        if not re.match("^[A-Za-z ]+$", name):
            messages.error(request, "Name should contain only letters.")
            return redirect("/order/?product_id=" + product_id)

        if not re.match("^[0-9]{10}$", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect("/order/?product_id=" + product_id)

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
        return redirect("/order/?product_id=" + product_id)

    context = {
        "product_name": product["name"] if product else "",
        "price": product["price"] if product else 0
    }

    return render(request, "order.html", context)


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    repairs = Repair.objects.filter(user=request.user)
    profile_obj = Profile.objects.filter(user=request.user).first()
    profile_image = profile_obj.image.url if profile_obj and profile_obj.image else None

    return render(request, "profile.html", {
        "orders": orders,
        "repairs": repairs,
        "profile_image": profile_image
    })


@login_required
def delete_order(request, id):
    order = Order.objects.get(id=id, user=request.user)
    order.delete()
    return redirect('profile')


@login_required
def delete_repair(request, id):
    repair = Repair.objects.get(id=id, user=request.user)
    repair.delete()
    return redirect('profile')


def update_order(request, id):

    order = get_object_or_404(Order, id=id)

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
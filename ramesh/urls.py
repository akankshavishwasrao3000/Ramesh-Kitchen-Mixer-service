from django.contrib import admin
from django.urls import path
from ramesh import views

urlpatterns = [
    path('', views.index, name='index'),   # Home page first

    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),

    path("products/", views.products, name='products'),
    path("services/", views.services, name='services'),
    path("contact/", views.contact, name='contact'),

    path("repair/", views.repair, name='repair'),
    path("order/", views.order, name='order'),

    path('profile/', views.profile, name='profile'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('update-order/<int:id>/', views.update_order, name='update_order'),
    path('delete-order/<int:id>/', views.delete_order, name='delete_order'),
    path('delete-repair/<int:id>/', views.delete_repair, name='delete_repair'),
]


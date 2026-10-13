from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Product
from .validators import validate_image_upload

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]


        widgets = {
    'first_name': forms.TextInput(attrs={'class':'form-control'}),
    'last_name': forms.TextInput(attrs={'class':'form-control'}),
    'username': forms.TextInput(attrs={'class':'form-control'}),
    'email': forms.EmailInput(attrs={'class':'form-control'}),
    'password1': forms.PasswordInput(attrs={'class':'form-control'}),
    'password2': forms.PasswordInput(attrs={'class':'form-control'}),
}
        

class OrderUpdateForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = Order
        fields = ['quantity']


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 150}),
        }


class ProfileImageForm(forms.Form):
    profile_image = forms.ImageField(validators=[validate_image_upload])


class OrderAdminForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False)
    quantity = forms.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = Order
        fields = [
            'product', 'user', 'name', 'phone', 'address', 'quantity',
            'order_status', 'delivery_days',
        ]

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if self.instance._state.adding and product is None:
            self.add_error('product', 'Select a product to reserve stock for this order.')
        elif self.instance._state.adding and product and not product.is_available:
            self.add_error('product', 'This product is unavailable.')
        elif (
            self.instance._state.adding
            and product
            and cleaned_data.get('quantity', 0) > product.stock
        ):
            self.add_error('quantity', 'The requested quantity is not available.')
        elif (
            not self.instance._state.adding
            and 'product' in self.fields
            and product != self.instance.product
        ):
            self.add_error('product', 'The product linked to an existing order cannot be changed.')
        return cleaned_data
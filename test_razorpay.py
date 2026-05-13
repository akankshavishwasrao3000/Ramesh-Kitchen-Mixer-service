import os
import django

# Setup django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
django.setup()

import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
try:
    razorpay_order = client.order.create({
        "amount": 100,
        "currency": "INR",
        "payment_capture": "1"
    })
    print("Order created:", razorpay_order)
except Exception as e:
    print("Error:", e)

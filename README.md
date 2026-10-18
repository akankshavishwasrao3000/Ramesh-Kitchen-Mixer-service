# Ramesh Kitchen Mixer Service

Ramesh Kitchen Mixer Service is a Django-based digital platform and service website for a local kitchen appliance business. The website lets customers browse products, place appliance orders, submit repair requests, and contact the business through WhatsApp for quick follow-up.

## Overview
This project was built to help a small local business move from manual order handling to a digital platform. It provides a clean digital storefront experience, secure user login, product management through the Django admin panel, and a WhatsApp-driven confirmation flow that suits a trust-based local sales model.

## Key Features
- User registration and login with Django authentication
- Product catalog stored in the database and displayed dynamically
- Product inventory and availability management through Django admin
- Order placement with quantity validation and stock checks
- Repair request form for service and maintenance inquiries
- WhatsApp order confirmation link generated after successful checkout
- Responsive frontend using Bootstrap 5
- Privacy, shipping, refund, and terms pages
- Cloud media storage support using Cloudinary
- Production-ready deployment configuration for Render and Railway

## Tech Stack
- Backend: Python, Django 4.2
- Database: MySQL
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Storage: Cloudinary
- Deployment: Gunicorn, WhiteNoise, Render/Railway-ready configuration
- Environment management: python-dotenv

## How the Application Works
1. Customers browse the product catalog from the database.
2. They choose a product, enter their details, and place an order.
3. The order is validated and saved with the current product price and quantity.
4. After a successful order, users are redirected to a confirmation page containing a WhatsApp message link.
5. Business owners can review and manage products, orders, and repair requests in the Django admin panel.
6. Repair requests are submitted through the customer support form and stored for business follow-up.

## Project Structure
```text
home/
├── home/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── certs/
├── ramesh/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── order_services.py
│   ├── templates/
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example (if present)
├── .gitignore
├── LICENSE
├── README.md
└── db.sqlite3
```

## Database Design
The application uses MySQL for persistent records and Django ORM for interacting with the database.

Main models include:
- Product: product name, price, stock, availability, description, and image
- Order: customer details, order amount, delivery, product reference, and status
- Repair: service request details, customer contact info, and city
- Profile: user-specific profile image and related account data

## Environment Variables
Create a `.env` file in the project root with variables similar to:

```env
SECRET_KEY=your_secret_key
DEBUG=True
MYSQL_DATABASE=ramesh_mixer_db
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

For production deployment, set the appropriate values for your hosting platform and include the live domain in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

## Local Setup

1. Clone the repository
```bash
git clone <repository-url>
cd home
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables in a `.env` file

5. Apply database migrations
```bash
python manage.py migrate
```

6. Create an admin user
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

The app will typically run at:
```text
http://127.0.0.1:8000/
```

## Admin Panel
Once the superuser is created, the admin interface is available at:
```text
http://127.0.0.1:8000/admin/
```

Use the admin panel to:
- add or update product listings
- manage stock and availability
- review customer orders
- monitor repair requests
- update order status

## Deployment Notes
This project includes production-ready settings for hosting on cloud providers. The app is configured to work with:
- MySQL database hosted remotely
- Cloudinary for media uploads
- WhiteNoise for static file serving
- Gunicorn for application serving

The `Procfile` includes a `collectstatic` step before the Django app starts, which is useful for deployment in containerized or platform-hosted environments.

## Future Enhancements
- online payment integration
- order tracking dashboard
- automated notifications and SMS/email alerts
- product search and category filters
- customer reviews and ratings
- expanded inventory management for spare parts
- mobile app support

## Author
Akanksha Ramesh Vishwasrao
B.E. Computer Engineering
Savitribai Phule Pune University (SPPU)

---
© 2026 Ramesh Kitchen Mixer Service. All rights reserved.

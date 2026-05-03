# 🍳 Ramesh Kitchen Mixer Service

A deployed Django business application for a kitchen mixer brand that combines product ordering, repair booking, customer support, and operations management in one platform.

This project is built to solve a real business need: local appliance retailers need a digital storefront and service workflow to modernize orders, repair requests, and customer communication.

---

## 🔥 Strong Project Introduction

Ramesh Kitchen Mixer Service replaces manual order ledgers and paper-based repair requests with a digital retail and support experience.

Customers can browse mixer models, place authenticated orders, and submit repair requests, while store staff can monitor users, manage orders, and update delivery status through a custom dashboard.

This is a genuine deployed business application with Railway hosting and production-ready deployment settings.

---

## ⚡ Key Highlights

- Live deployment on Railway
- PostgreSQL-ready production database support
- Custom staff dashboard for user and order management
- Local chatbot assistant from `static/script.js`
- Protected user profile showing orders and repairs
- WhiteNoise static file delivery and secure production settings

---

## 🧠 Complete Project Flow

### Customer flow

1. Visitor reaches the homepage and navigates to products, repair, services, or contact pages.
2. User signs up or logs in with Django authentication.
3. From `products.html`, the customer selects a mixer and is routed to `/order/?product_id=<id>`.
4. The order page shows hard-coded product pricing and calculates the total dynamically.
5. The user submits name, phone, address, and quantity.
6. The app validates input, saves the order in the `Order` model, and redirects back to the order page.
7. Logged-in users can view orders and repairs on `profile.html`, update quantity, cancel orders, upload a profile image, or delete repair entries.

### Repair flow

1. Authenticated user visits `/repair/`.
2. The repair form collects name, mobile, email, city, and issue description.
3. Valid repair requests are stored in the `Repair` model.
4. Repair records appear on the profile page for tracking and cleanup.

### Admin flow

1. Staff or superuser accesses `/dashboard/`.
2. The dashboard lists all registered users.
3. Admin views a specific user’s orders at `/dashboard/user/<id>/`.
4. Admin updates an order’s status using `Order.STATUS_CHOICES` and persists the change.
5. The updated status is visible in the user’s order history and profile.

---

## ✨ Features (Based on Code)

### Customer features

- Signup and login pages with secure authentication
- Authenticated profile page with personal order and repair history
- Profile image upload using `Profile` model
- Order placement with product selection, quantity validation, and total price calculation
- Repair request submission with validation and persistent storage

### Order and repair management

- `Order` model includes product name, price, quantity, total, status, and delivery estimate
- Default order status is `Processing`
- Users can update order quantity and cancel orders from their profile
- Repair requests can be created and removed by customers

### Admin capabilities

- Staff-only dashboard for listing all users
- User detail page showing orders and status update form
- Order status update workflow using dashboard forms
- Admin access protection via `is_staff` / `is_superuser`

### Chatbot and support

- Local chatbot UI integrated in `templates/base.html`
- Rule-based responses for orders, delivery, repairs, payment options, and contact
- Real-time chat interface implemented in `static/script.js`

---

## 🏗️ System Architecture

- **Frontend:** Django templates + Bootstrap 5 + custom CSS/JavaScript
- **Backend:** Django views, forms, models, auth, and messaging
- **Models:** `Order`, `Repair`, `Profile` linked to Django `User`
- **Database:** PostgreSQL via `DATABASE_URL`; SQLite fallback for local development
- **Deployment:** Railway-ready with environment variables and WhiteNoise static serving

---

## 🛠️ Tech Stack

| Technology | Purpose |
| --- | --- |
| Django 4.2 | Web application framework |
| Python | Backend logic |
| PostgreSQL | Production database support |
| SQLite | Local development fallback |
| Bootstrap 5 | Responsive UI styling |
| WhiteNoise | Static asset delivery |
| Railway | Deployment platform |
| python-dotenv | Environment configuration |

---

## 🔐 Security Features

- Environment-based `SECRET_KEY` management
- Production-ready `DEBUG=False` support
- `SECURE_SSL_REDIRECT` when not in debug mode
- `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` enabled in production
- HSTS enforcement via `SECURE_HSTS_SECONDS`
- `SECURE_CONTENT_TYPE_NOSNIFF` enabled
- `X_FRAME_OPTIONS = 'DENY'`
- `CSRF_TRUSTED_ORIGINS` loaded from environment variables

> No secrets, credentials, or passwords are exposed in this repository.

---

## ⚙️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/akankshavishwasrao3000/Ramesh-Kitchen-Mixer-service.git
cd home
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file at the project root:

```env
SECRET_KEY=your_secret_key_here
DEBUG=False
DATABASE_URL=postgres://user:password@host:port/dbname
ALLOWED_HOSTS=ramesh-kitchen-mixer-service-production.up.railway.app,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://ramesh-kitchen-mixer-service-production.up.railway.app,http://127.0.0.1:8000,http://localhost:8000
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

---

## 🌍 Live Demo + Repository

- **Live Demo:** https://ramesh-kitchen-mixer-service-production.up.railway.app
- **GitHub:** https://github.com/akankshavishwasrao3000/Ramesh-Kitchen-Mixer-service

---

## 👨‍💻 Author

- **Name:** Akanksha Vishwasrao
- **Role:** Final Year Student / Django Developer
- **Project Type:** Real Business Application

---

## 🎯 What I Learned

- Building a deployed Django application for a real local business
- Securing Django deployment settings for Railway and PostgreSQL
- Implementing authenticated order and repair workflows
- Creating a staff dashboard for user and order operations
- Adding a local chatbot assistant and profile image uploads

---

## 🚀 Future Improvements

- Add payment gateway integration (Stripe / Razorpay)
- Upgrade chatbot to AI/NLP-based support
- Add email and SMS notifications for order and repair updates
- Implement inventory and product catalog management
- Add repair request tracking and technician assignment

---

## � License

This project is available for portfolio and demonstration use. Feel free to adapt the code while keeping attribution to the original author. For commercial use, please contact the author for licensing details.

---
⚠️ Important Notice
This project "Ramesh Kitchen Mixer Service" is developed by Akanksha Ramesh Vishwasrao.

This project is licensed under the MIT License.

Proper credit must be given when using or modifying this project.

Please do not claim this project as your own work.

## �📌 Notes

This README reflects the real application code and behavior present in the repository.

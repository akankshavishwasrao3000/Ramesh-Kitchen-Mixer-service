# Ramesh Kitchen Mixer 🌪️

Ramesh Kitchen Mixer is a Django-based business website developed for a local mixer repair and sales business. The platform allows customers to explore products, submit repair requests, place orders, and communicate directly through WhatsApp. The project focuses on digital business growth and customer engagement.

## 📌 Problem Statement
Local businesses often struggle to reach a wider audience and manage service requests efficiently. "Ramesh Kitchen Mixer" addresses this by providing a digital storefront where customers can view high-quality kitchen appliances, book professional repairs, and place orders with direct WhatsApp integration for seamless manual confirmation, replacing traditional complex payment gateways with a trust-based local model.

## ✨ Features
*   **User Authentication**: Secure registration and login system for customers to track their activity.
*   **Product Catalog**: Modern display of available kitchen mixers and spare parts with detailed specifications.
*   **Order Management**: Simple order form that saves data to the database and redirects to WhatsApp for final confirmation.
*   **Repair Requests**: Dedicated module for users to book mixer repair services with problem descriptions.
*   **AI Mixer Assistant**: A rule-based, lightweight chatbot to guide users through pricing, services, and location queries.
*   **WhatsApp Integration**: Automatic message generation containing order/product details for quick business communication.
*   **Admin Dashboard**: Powerful Django admin interface for the owner to manage products, view orders, and update statuses.
*   **Modern UI/UX**: Responsive design using Bootstrap 5, featuring sleek animations and a professional aesthetic.
*   **Policy Pages**: Professional Privacy Policy, Terms & Conditions, and Shipping policies tailored for a local business.

## ⚙️ System Workflow (How it Works)
*   **User Authentication**: The system uses Django’s built-in authentication system. Users can create a secure account, log in, and access their private profile to manage their orders and repair history.
*   **Order Process**: When a user selects a product, they fill out an order form. Once submitted, the data is instantly saved in the **MySQL database**, and the user is redirected to **WhatsApp** with a pre-filled message containing their order details for final confirmation with the owner.
*   **Repair Requests**: Customers can submit an online request detailing their mixer issues. These requests are stored in the database and displayed in the **Admin Panel** for the shop owner to review and manage.
*   **Centralized Management**: The shop owner uses the **Django Admin Panel** to monitor all user activity, update order statuses (e.g., from Processing to Delivered), and manage the product inventory efficiently.

## 🛠️ Technologies Used
*   **Backend**: Python, Django 4.2
*   **Database**: MySQL (Production/Local), SQLite (Backup)
*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5
*   **Authentication**: Django Auth System
*   **Environment Management**: Python-dotenv
*   **Styling**: Font Awesome, Google Fonts, Bootstrap Icons

## 📂 Project Structure
```text
home/
├── home/                   # Project Configuration
│   ├── settings.py         # Global Settings
│   ├── urls.py             # Main Route Mapping
│   └── wsgi.py             # Web Server Entry Point
├── ramesh/                 # Main Business Application
│   ├── models.py           # Database Schemas (Order, Repair, Profile)
│   ├── views.py            # Business Logic & Request Handling
│   ├── urls.py             # App-specific Routes
│   ├── admin.py            # Admin Panel Configurations
│   └── forms.py            # User Input Validation
├── templates/              # HTML Templates (Bootstrap 5)
├── static/                 # Static Assets (CSS, JS, Images)
├── media/                  # User Uploads (Profile Images)
├── requirements.txt        # Project Dependencies
├── .env                    # Environment Variables (Sensitive)
└── manage.py               # Django Management Script
```

## 🗄️ Database Information
The project utilizes a **MySQL** database for robust data management.
*   **Order Model**: Stores customer details, product info, and order status.
*   **Repair Model**: Tracks service requests and customer contact info.
*   **Profile Model**: Handles user-specific data and profile images.

## 🚀 Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd project-folder
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Admin)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Server**:
   ```bash
   python manage.py runserver
   ```


## 🔮 Future Enhancements
*   **Payment Gateway**: Integration with Razorpay for automated online payments.
*   **Order Tracking**: Real-time status updates for orders and repairs.
*   **Notifications**: Automated email and SMS notifications for customers.
*   **Search & Filter**: Advanced product search and category filtering.
*   **Customer Reviews**: Ratings and review system for products and services.
*   **Inventory**: Automated stock management for spare parts.
*   **Mobile App**: Dedicated Android/iOS application for easier access.

## 👤 Author
Author: Akanksha Ramesh Vishwasrao
B.E. Computer Engineering
Savitribai Phule Pune University (SPPU)

---
© 2026 Ramesh Kitchen Mixer. All Rights Reserved.

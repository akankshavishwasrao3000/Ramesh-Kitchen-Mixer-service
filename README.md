# Ramesh Kitchen Mixer – E-Commerce & Service Platform

A full-stack web application built with Django that allows customers to explore kitchen mixers, place orders, and book repair services online. The platform also includes user authentication, a customer profile dashboard, and a simple chatbot to assist users with common questions about products and services.

## 📚 Table of Contents

- Project Overview
- Key Features
- Technologies & Stack
- Database Models
- CRUD Operations
- Project Structure
- URL Routes
- Security Features
- Getting Started
- Usage Instructions
- Dependencies
- Future Improvements
- Contact
- Author
## 🎯 Project Overview

Ramesh Kitchen Mixer is a complete e-commerce and service platform that enables customers to:
- Browse and purchase kitchen mixers online
- Book mixer repair services
- Track their orders and repair requests
- Manage their account profile
- Access product information and customer support via AI chatbot

**Live Site**: [rameshservices.pythonanywhere.com](http://rameshservices.pythonanywhere.com)

## ✨ Key Features

### Authentication & Account Management
- User registration with email and password
- Secure login/logout functionality
- User profile dashboard
- Django admin panel for business operations

### E-Commerce Features
- Product catalog with 4 mixer models
- Dynamic order placement with quantity selection
- Price calculation and total amount display
- Order history and management
- Order cancellation capability


### Service Booking
- Repair request form with customer details
- Problem description capturing
- Repair request history tracking
- Request cancellation option

### Customer Support
- AI-powered chatbot with keyword-based responses
- Answers about pricing, ordering, repairs, warranty, location
- Floating chat widget on all pages
- Persistent chat message history

### Frontend
- Responsive Bootstrap 5 design
- Product image carousel
- User-friendly forms with validation
- Mobile-optimized navigation
- Professional branding and styling

## 🛠 Technologies & Stack

### Backend
- **Framework**: Django 4.2
- **Language**: Python 3.8+
- **Database**: MySQL
- **Environment**: python-dotenv

### Frontend
- **CSS Framework**: Bootstrap 5.3.2
- **JavaScript**: Vanilla JavaScript
- **Icons**: Bootstrap Icons
- **CDN**: jsDelivr

### Deployment
- **Host**: PythonAnywhere
- **Database**: MySQL (remote)
- **Web Server**: PythonAnywhere WSGI

## 🗄️ Database Models

### Repair Model
- name, email, mobile, city, description
- created_at timestamp
- Link to User account

### Order Model
- product_name, name, phone, address
- price, quantity, total
- created_at timestamp
- Link to User account

## 🚀 Getting Started

### Installation

1. Clone or download the project:
   ```bash
   cd Djangoharry/home
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django==4.2
   pip install mysqlclient  # or mysql-connector-python
   pip install python-dotenv
   ```

4. Create `.env` file in project root:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=your_database_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create superuser (for admin panel):
   ```bash
   python manage.py createsuperuser
   ```

7. Start development server:
   ```bash
   python manage.py runserver
   ```

Access the application at `http://127.0.0.1:8000/`

## 📝 Usage Instructions

### For Customers

1. **Create Account**: Click "Sign Up" and fill in your details
2. **Login**: Enter your credentials
3. **Browse Products**: View mixer catalog on Products page
4. **Place Order**: Click "Order Now" on desired mixer, confirm details
5. **Book Repair**: Go to "Book Repair", describe your issue
6. **Manage Account**: Visit Profile to view orders and repair requests
7. **Use Chatbot**: Click the blue chat icon for instant customer support

### For Admin

1. Access admin panel at `/admin/`
2. View all orders and repair requests
3. Monitor customer data
4. Manage product information

## � CRUD Operations

### Create (C)
- **User Registration**: New users can sign up with email and password
- **Place Orders**: Authenticated users can create new orders for kitchen mixers
  - Route: `/order/`
  - Requires: Product selection, quantity, delivery address, phone number
  - Validation: Name (letters only), Phone (10 digits)
- **Book Repair Services**: Users can create repair requests with problem details
  - Route: `/repair/`
  - Requires: Name, email, mobile, city, problem description
  - Auto-timestamps requests

### Read (R)
- **View Orders**: Users can view all their placed orders in profile
  - Route: `/profile/`
  - Displays: Product name, quantity, price, total, order date
- **View Repair Requests**: Users can see all their repair requests with details
  - Route: `/profile/`
  - Displays: Customer info, problem description, request date
- **Browse Products**: Public access to view all available mixer models
  - Route: `/products/`
- **View Services & Contact Info**: Public access to service details and support information

### Update (U)
- **Limited Update Capability**: Current version doesn't support direct order/repair updates
- **Future Enhancement**: Could implement edit functionality for pending repairs

### Delete (D)
- **Cancel Orders**: Users can delete their orders from profile
  - Route: `/delete-order/<id>/`
  - Only order owner can delete
  - Cascades with user account deletion
- **Cancel Repair Requests**: Users can delete their repair requests
  - Route: `/delete-repair/<id>/`
  - Only request owner can delete
  - Cascades with user account deletion

## �📁 Project Structure

```
home/
├── manage.py                 # Django management script
├── home/                     # Project settings
│   ├── settings.py          # Configuration
│   ├── urls.py              # Main URL router
│   └── wsgi.py              # Production server
├── ramesh/                  # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Registration form
│   ├── urls.py              # App routes
│   ├── admin.py             # Admin config
│   └── migrations/          # Database migrations
├── templates/               # HTML templates (10 files)
├── static/                  # CSS, JavaScript, images
└── db.sqlite3              # SQLite database
```

## 🔄 URL Routes

| Route | Purpose | Authentication |
|-------|---------|-----------------|
| `/` | Home page | Public |
| `/products/` | Product listing | Public |
| `/services/` | Service information | Public |
| `/contact/` | Contact details | Public |
| `/login/` | User login | Public |
| `/signup/` | User registration | Public |
| `/logout/` | User logout | Required |
| `/order/` | Place order | Required |
| `/repair/` | Book repair | Required |
| `/profile/` | User dashboard | Required |
| `/admin/` | Admin panel | Staff |

## 🔐 Security Features

- CSRF protection enabled
- Password validation and hashing
- Environment-based configuration for secrets
- User authentication decorators
- Per-user data access control

## 🎨 Features Detail

### Order System
- Select mixer model and quantity
- View real-time total price calculation
- Validation: Name (letters only), Phone (10 digits)
- Order confirmation and history tracking

### Repair System
- Multi-field repair request form
- Problem description capture
- City and contact information
- Automated timestamp recording

### User Profile
- View all placed orders with details
- View all repair requests
- Cancel orders and repair requests
- Personal information display

## 📦 Dependencies

```
Django==4.2
mysqlclient==2.x or mysql-connector-python==8.x
python-dotenv==0.x
```

## 🐛 Known Issues & Future Improvements

- Unused imports (matplotlib, requests) can be removed
- Products stored as dictionary - consider moving to database model
- Consider adding payment gateway integration
- Email notifications for orders could be implemented
- ChatBot can be enhanced with machine learning

## 🤝 Contact & Support

- **Phone**: +91 9921071945
- **WhatsApp**: Chat directly
- **Instagram**: @ramesh_kitchen_mixer
- **Location**: Belhe, Tal: Junnar, Dist: Pune

## 📄 License

Private project for Ramesh Kitchen Mixer business.

## 👨‍💼 Author

Author
Akanksha Vishwasrao
BE. Computer Engineering Student
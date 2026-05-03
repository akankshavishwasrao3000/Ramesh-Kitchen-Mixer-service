from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Order, Repair


class AppFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='Testpass123',
            first_name='John',
            last_name='Doe',
        )
        self.staff_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='Testpass123',
            is_staff=True,
        )

    def test_signup_creates_account(self):
        response = self.client.post(
            reverse('signup'),
            {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'username': 'janedoe',
                'email': 'jane@example.com',
                'password1': 'Testpass123',
                'password2': 'Testpass123',
            },
        )
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='janedoe').exists())

    def test_login_and_logout_flow(self):
        logged_in = self.client.login(username='john', password='Testpass123')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_order_creation_works(self):
        self.client.login(username='john', password='Testpass123')
        response = self.client.post(
            f"{reverse('order')}?product_id=1",
            {
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '2',
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user, product_name='Ramesh Mixer 1').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total, order.price * order.quantity)

    def test_repair_request_works(self):
        self.client.login(username='john', password='Testpass123')
        response = self.client.post(
            reverse('repair'),
            {
                'name': 'John Doe',
                'mobile': '9876543210',
                'email': 'john@example.com',
                'city': 'Test City',
                'description': 'Mixer is not working.',
            },
        )
        self.assertEqual(response.status_code, 302)
        repair = Repair.objects.filter(user=self.user, name='John Doe').first()
        self.assertIsNotNone(repair)

    def test_dashboard_access_control(self):
        self.client.login(username='john', password='Testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('index'))

        self.client.logout()
        self.client.login(username='adminuser', password='Testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

    def test_chatbot_script_is_present(self):
        script_path = Path(settings.BASE_DIR) / 'static' / 'script.js'
        self.assertTrue(script_path.exists())
        self.assertIn('function getBotResponse', script_path.read_text(encoding='utf-8'))

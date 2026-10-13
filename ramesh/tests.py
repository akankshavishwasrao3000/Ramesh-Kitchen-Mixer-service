from io import BytesIO
from decimal import Decimal
from pathlib import Path
import re
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import ProfileImageForm
from .models import Order, Product, Profile, Repair
from .order_services import create_order, delete_order
from .validators import MAX_IMAGE_SIZE, validate_image_upload


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
            is_superuser=True,
        )
        self.product = Product.objects.create(
            name='Ramesh Mixer 1',
            slug='ramesh-mixer-1',
            description='<ul><li>900W powerful motor</li><li>3 stainless steel jars</li></ul>',
            price='3500.00',
            stock=10,
            is_available=True,
        )

    def test_product_features_render_as_html(self):
        response = self.client.get(reverse('products'), follow=True)

        self.assertIn(b'<ul>', response.content)
        self.assertIn(b'<li>900W powerful motor</li>', response.content)
        self.assertIn(b'<li>3 stainless steel jars</li>', response.content)
        self.assertContains(response, 'Sign in to order')
        self.assertNotContains(response, 'Search products by name')
        self.assertNotContains(response, 'id="product-search"')

    def test_homepage_keeps_database_products_on_catalog_only(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.name)
        self.assertContains(response, reverse('products'))
        self.assertContains(response, 'category-card-image')

    def test_catalog_shows_products_without_search_sort_or_availability_controls(self):
        sold_out_product = Product.objects.create(
            name='Ramesh Mini Mixer',
            slug='ramesh-mini-mixer',
            price='1200.00',
            stock=0,
            is_available=True,
        )
        response = self.client.get(
            reverse('products'),
            {'q': 'mini', 'availability': 'sold-out', 'sort': 'price-desc'},
        )
        self.assertContains(response, sold_out_product.name)
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, 'product-catalog-filters')
        self.assertNotContains(response, 'availability-filter')
        self.assertNotContains(response, 'sort-products')
        self.assertNotContains(response, 'Clear filters')

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

    def test_signup_page_does_not_render_product_catalog(self):
        response = self.client.get(reverse('signup'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product.name)
        self.assertContains(response, 'Create Account')
        for label in ('First Name', 'Last Name', 'Username', 'Email', 'Password', 'Confirm Password'):
            self.assertContains(response, label)
        self.assertContains(response, 'Create Account</button>')
        self.assertContains(response, '/static/logo.')
        self.assertContains(response, 'background-image: none;')

    def test_login_page_has_readable_labels_button_and_site_logo(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username</label>')
        self.assertContains(response, 'Password</label>')
        self.assertContains(response, 'Sign In</button>')
        self.assertContains(response, '/static/logo.')

    def test_login_and_logout_flow(self):
        logged_in = self.client.login(username='john', password='Testpass123')
        self.assertTrue(logged_in)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_login_returns_to_safe_order_url_but_rejects_external_next(self):
        order_url = f"{reverse('order')}?product_id={self.product.pk}"
        response = self.client.post(
            reverse('login'),
            {
                'username': 'john',
                'password': 'Testpass123',
                'next': order_url,
            },
        )
        self.assertRedirects(response, order_url)

        self.client.get(reverse('logout'))
        response = self.client.post(
            reverse('login'),
            {
                'username': 'john',
                'password': 'Testpass123',
                'next': 'https://example.com/',
            },
        )
        self.assertRedirects(response, reverse('index'))

    def test_order_creation_works(self):
        self.client.login(username='john', password='Testpass123')
        response = self.client.post(
            f"{reverse('order')}?product_id={self.product.id}",
            {
                'product_id': str(self.product.id),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '2',
                'price': '1.00',
                'total': '2.00',
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user, product_name='Ramesh Mixer 1').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.price, self.product.price)
        self.assertEqual(order.total, order.price * order.quantity)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.reserved_quantity, 2)

    def test_unavailable_product_and_invalid_or_insufficient_quantity_are_rejected(self):
        self.client.login(username='john', password='Testpass123')
        self.product.is_available = False
        self.product.save()
        response = self.client.post(
            reverse('order'),
            {
                'product_id': str(self.product.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '1',
            },
        )
        self.assertRedirects(response, reverse('products'))
        self.assertFalse(Order.objects.exists())
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 10)

        self.product.is_available = True
        self.product.stock = 1
        self.product.save()
        response = self.client.post(
            reverse('order'),
            {
                'product_id': str(self.product.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '2',
            },
        )
        self.assertRedirects(response, reverse('products'))
        self.assertFalse(Order.objects.exists())
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 1)

        response = self.client.post(
            reverse('order'),
            {
                'product_id': str(self.product.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '0',
            },
        )
        self.assertRedirects(response, f"{reverse('order')}?product_id={self.product.pk}")
        self.assertFalse(Order.objects.exists())

    def test_order_quantity_changes_adjust_inventory_and_keep_price_snapshot(self):
        self.client.login(username='john', password='Testpass123')
        self.client.post(
            f"{reverse('order')}?product_id={self.product.pk}",
            {
                'product_id': str(self.product.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '2',
            },
        )
        order = Order.objects.get(user=self.user)
        Product.objects.filter(pk=self.product.pk).update(price='4000.00')

        response = self.client.post(
            reverse('update_order', args=[order.pk]),
            {'quantity': '5'},
        )
        self.assertRedirects(response, reverse('profile'))
        order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(order.total, order.price * 5)
        self.assertEqual(order.price, Decimal('3500.00'))
        self.assertEqual(order.reserved_quantity, 5)
        self.assertEqual(self.product.stock, 5)

        self.client.post(
            reverse('update_order', args=[order.pk]),
            {'quantity': '1'},
        )
        order.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(order.reserved_quantity, 1)
        self.assertEqual(self.product.stock, 9)

    def test_order_cancellation_restores_stock_once(self):
        order = create_order(
            product_id=self.product.pk,
            user=self.user,
            name='John Doe',
            phone='9876543210',
            address='123 Main Street',
            quantity=3,
        )
        self.client.login(username='john', password='Testpass123')
        response = self.client.post(reverse('delete_order', args=[order.pk]))
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 10)
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())
        response = self.client.post(reverse('delete_order', args=[order.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 10)

    def test_order_creation_rolls_back_when_stock_save_fails(self):
        from unittest.mock import patch

        with patch.object(Product, 'save', side_effect=RuntimeError('stock write failed')):
            with self.assertRaises(RuntimeError):
                create_order(
                    product_id=self.product.pk,
                    user=self.user,
                    name='John Doe',
                    phone='9876543210',
                    address='123 Main Street',
                    quantity=2,
                )
        self.assertFalse(Order.objects.exists())
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 10)

    def test_deletes_are_post_only_csrf_protected_and_check_ownership(self):
        own_repair = Repair.objects.create(
            user=self.user,
            name='John Doe',
            email='john@example.com',
            mobile='9876543210',
            city='Test City',
            description='Repair this mixer.',
        )
        self.client.login(username='john', password='Testpass123')
        self.assertEqual(
            self.client.get(reverse('delete_repair', args=[own_repair.pk])).status_code,
            405,
        )

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(
            csrf_client.post(reverse('delete_repair', args=[own_repair.pk])).status_code,
            403,
        )

        other_repair = Repair.objects.create(
            user=self.staff_user,
            name='Admin',
            email='admin@example.com',
            mobile='9876543210',
            city='Test City',
            description='Another user repair.',
        )
        response = self.client.post(reverse('delete_repair', args=[other_repair.pk]))
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(Repair.objects.filter(pk=other_repair.pk).exists())

        order = create_order(
            product_id=self.product.pk,
            user=self.user,
            name='John Doe',
            phone='9876543210',
            address='123 Main Street',
            quantity=2,
        )
        self.assertEqual(
            self.client.get(reverse('delete_order', args=[order.pk])).status_code,
            405,
        )
        self.assertEqual(
            csrf_client.post(reverse('delete_order', args=[order.pk])).status_code,
            403,
        )
        self.assertTrue(Order.objects.filter(pk=order.pk).exists())

        other_order = create_order(
            product_id=self.product.pk,
            user=self.staff_user,
            name='Admin',
            phone='9876543210',
            address='Another address',
            quantity=1,
        )
        self.client.post(reverse('delete_order', args=[other_order.pk]))
        self.assertTrue(Order.objects.filter(pk=other_order.pk).exists())

    def test_profile_information_updates_only_current_user(self):
        other_user = User.objects.create_user(
            username='jane',
            email='jane@example.com',
            password='Testpass123',
        )
        self.client.login(username='john', password='Testpass123')
        response = self.client.post(
            reverse('profile'),
            {'first_name': 'Updated', 'last_name': 'Name', 'email': 'updated@example.com'},
        )
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        other_user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(other_user.email, 'jane@example.com')

    def test_admin_order_creation_and_quantity_edit_use_inventory_service(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(
            '/admin/ramesh/order/add/',
            {
                'product': str(self.product.pk),
                'user': str(self.user.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '2',
                'order_status': 'Processing',
                'delivery_days': '3-7 days',
                '_save': 'Save',
            },
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.price, self.product.price)
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 8)

        response = self.client.post(
            f'/admin/ramesh/order/{order.pk}/change/',
            {
                'user': str(self.user.pk),
                'name': 'John Doe',
                'phone': '9876543210',
                'address': '123 Main Street',
                'quantity': '4',
                'order_status': 'Processing',
                'delivery_days': '3-7 days',
                '_save': 'Save',
            },
        )
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.quantity, 4)
        self.assertEqual(order.total, order.price * 4)
        self.assertEqual(Product.objects.get(pk=self.product.pk).stock, 6)

    def test_nullable_user_order_does_not_break_dashboard(self):
        Order.objects.create(
            product_name='Historical mixer',
            name='Legacy Customer',
            phone='9876543210',
            address='Old address',
            price='100.00',
            quantity=1,
            total='100.00',
        )
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


def make_test_image(name='test.png', image_format='PNG'):
    image_buffer = BytesIO()
    Image.new('RGB', (2, 2), color='teal').save(image_buffer, format=image_format)
    return SimpleUploadedFile(
        name,
        image_buffer.getvalue(),
        content_type=f'image/{image_format.lower()}',
    )


class ImageHandlingTests(TestCase):
    def setUp(self):
        self.temp_directory = TemporaryDirectory()
        self.media_settings = override_settings(MEDIA_ROOT=self.temp_directory.name)
        self.media_settings.enable()
        self.user = User.objects.create_user(
            username='imageuser',
            email='image@example.com',
            password='Testpass123',
        )
        self.staff_user = User.objects.create_user(
            username='imagestaff',
            email='staff@example.com',
            password='Testpass123',
            is_staff=True,
            is_superuser=True,
        )
        self.product = Product.objects.create(
            name='Image test mixer',
            slug='image-test-mixer',
            price='3500.00',
            stock=10,
            is_available=True,
        )

    def tearDown(self):
        self.media_settings.disable()
        self.temp_directory.cleanup()

    def test_profile_save_without_image_change_preserves_file(self):
        profile = Profile.objects.create(user=self.user, image=make_test_image())
        existing_name = profile.image.name
        existing_path = profile.image.path

        profile.save()

        self.assertEqual(profile.image.name, existing_name)
        self.assertTrue(Path(existing_path).exists())

    def test_profile_image_replacement_deletes_old_file_after_save(self):
        profile = Profile.objects.create(user=self.user, image=make_test_image())
        old_name = profile.image.name
        old_path = profile.image.path

        with self.captureOnCommitCallbacks(execute=True):
            profile.image = make_test_image('replacement.png')
            profile.save()

        self.assertNotEqual(profile.image.name, old_name)
        self.assertTrue(Path(profile.image.path).exists())
        self.assertFalse(Path(old_path).exists())

    def test_profile_replacement_keeps_old_file_when_another_record_references_it(self):
        profile = Profile.objects.create(user=self.user, image=make_test_image())
        old_name = profile.image.name
        old_path = profile.image.path
        Product.objects.create(
            name='Shared image product',
            slug='shared-image-product',
            price='100.00',
            stock=1,
            image=old_name,
        )

        with self.captureOnCommitCallbacks(execute=True):
            profile.image = make_test_image('replacement.png')
            profile.save()

        self.assertTrue(Path(old_path).exists())
        self.assertEqual(Product.objects.get(slug='shared-image-product').image.name, old_name)

    def test_product_image_replacement_preserves_unrelated_updates_and_deletes_old_file(self):
        product = Product.objects.create(
            name='Image replacement mixer',
            slug='image-replacement-mixer',
            price='100.00',
            stock=1,
            image=make_test_image('product-original.png'),
        )
        old_name = product.image.name
        old_path = product.image.path

        product.stock = 2
        product.save(update_fields=['stock'])
        self.assertEqual(product.image.name, old_name)
        self.assertTrue(Path(old_path).exists())

        with self.captureOnCommitCallbacks(execute=True):
            product.image = make_test_image('product-replacement.png')
            product.save()

        self.assertNotEqual(product.image.name, old_name)
        self.assertTrue(Path(product.image.path).exists())
        self.assertFalse(Path(old_path).exists())

    def test_invalid_and_oversized_profile_uploads_are_rejected_without_erasing_image(self):
        profile = Profile.objects.create(user=self.user, image=make_test_image())
        old_name = profile.image.name
        old_path = profile.image.path
        client = Client()
        client.force_login(self.user)

        invalid_response = client.post(
            reverse('upload_profile_image'),
            {'profile_image': SimpleUploadedFile('invalid.png', b'not an image')},
        )
        self.assertRedirects(invalid_response, reverse('profile'))
        profile.refresh_from_db()
        self.assertEqual(profile.image.name, old_name)
        self.assertTrue(Path(old_path).exists())

        oversized = SimpleUploadedFile(
            'oversized.png',
            b'x' * (MAX_IMAGE_SIZE + 1),
            content_type='image/png',
        )
        form = ProfileImageForm(files={'profile_image': oversized})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('profile_image'))

    def test_product_image_and_missing_image_fallback_render(self):
        image_product = Product.objects.create(
            name='Mixer with image',
            slug='mixer-with-image',
            price='100.00',
            stock=2,
            image=make_test_image('product.png'),
        )
        fallback_product = Product.objects.create(
            name='Mixer without image',
            slug='mixer-without-image',
            price='200.00',
            stock=1,
        )

        response = self.client.get(reverse('products'))

        self.assertContains(response, image_product.image.url)
        self.assertContains(response, 'Mixer without image')
        self.assertFalse(fallback_product.image)
        self.assertContains(response, static('mixer1.jpg'))
        self.assertContains(response, image_product.name)
        self.assertContains(response, fallback_product.name)

    def test_uploaded_profile_image_is_assigned_to_authenticated_user(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(
            reverse('upload_profile_image'),
            {'profile_image': make_test_image('profile.png')},
        )

        self.assertRedirects(response, reverse('profile'))
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(Path(profile.image.path).exists())
        self.assertContains(client.get(reverse('profile')), profile.image.url)

    def test_image_validator_rejects_oversized_upload_before_decoding(self):
        oversized = SimpleUploadedFile(
            'oversized.png',
            b'x' * (MAX_IMAGE_SIZE + 1),
            content_type='image/png',
        )
        with self.assertRaisesMessage(ValidationError, 'Image files must be 5 MB or smaller.'):
            validate_image_upload(oversized)

    def test_order_page_requires_authentication_and_preserves_selected_product(self):
        response = self.client.get(
            reverse('order'),
            {'product_id': self.product.pk},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response['Location'])
        self.assertIn(reverse('order'), response['Location'])
        self.assertIn(f'product_id%3D{self.product.pk}', response['Location'])

    def test_authenticated_customer_can_open_order_form_for_a_product(self):
        self.client.login(username='imageuser', password='Testpass123')
        response = self.client.get(
            reverse('order'),
            {'product_id': self.product.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, str(self.product.price))

    def test_repair_request_works(self):
        self.client.login(username='imageuser', password='Testpass123')
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
        self.client.login(username='imageuser', password='Testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('index'))

        self.client.logout()
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to your')
        self.assertContains(response, 'dashboardShowreel')
        self.assertContains(response, 'Ramesh mixer grinder in a warm home kitchen')

    def test_staff_can_update_order_status_with_csrf_protection_enabled(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            product_name=self.product.name,
            name='John Doe',
            phone='9876543210',
            address='123 Main Street',
            price=self.product.price,
            quantity=1,
            total=self.product.price,
        )
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.staff_user)

        response = csrf_client.get(reverse('user_detail', args=[self.user.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('no-store', response['Cache-Control'])
        token_match = re.search(
            rb'name="csrfmiddlewaretoken" value="([^"]+)"',
            response.content,
        )
        self.assertIsNotNone(token_match)
        response = csrf_client.post(
            reverse('update_order_status', args=[order.pk]),
            {
                'csrfmiddlewaretoken': token_match.group(1).decode(),
                'order_status': 'Delivered',
            },
        )

        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.order_status, 'Delivered')

    def test_services_page_uses_mixer_image_hero_instead_of_blue_banner(self):
        response = self.client.get(reverse('services'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'services-showreel')
        self.assertContains(response, 'Ramesh mixer in a warm, sunlit kitchen')
        self.assertNotContains(response, 'services-hero bg-primary')

    def test_login_and_signup_pages_have_no_fullscreen_image_background(self):
        login_response = self.client.get(reverse('login'))
        signup_response = self.client.get(reverse('signup'))

        for response in (login_response, signup_response):
            self.assertContains(response, 'class="auth-screen"')
            self.assertNotContains(response, 'auth-backdrop')
            for image_name in ('rm1.', 'rm2.', 'rm3.'):
                self.assertNotContains(response, f'/static/{image_name}')

    def test_chatbot_script_is_present(self):
        script_path = Path(settings.BASE_DIR) / 'static' / 'script.js'
        self.assertTrue(script_path.exists())
        self.assertIn('function getBotResponse', script_path.read_text(encoding='utf-8'))

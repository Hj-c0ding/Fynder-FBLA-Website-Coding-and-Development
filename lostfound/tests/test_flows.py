from datetime import date

from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ..models import ClaimRequest, Item


class LostFoundFlowTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.staff = User.objects.create_user(
			username='staff1',
			password='testpass123',
			is_staff=True,
		)

	def test_admin_login_page_links_back_to_main_site(self):
		response = self.client.get('/admin/login/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, reverse('home'))
		self.assertContains(response, 'aria-label="Back to main website"')
		self.assertContains(response, '&larr;')

	def test_report_item_creates_pending_submission(self):
		response = self.client.post(
			reverse('report_item'),
			{
				'title': 'Black Water Bottle',
				'category': 'accessories',
				'description': 'Metal bottle with school sticker.',
				'location_found': 'Gym entrance',
				'date_found': '2026-03-17',
				'submitted_by_name': 'Alex Rivera',
				'submitted_by_email': 'alex@example.com',
				'submitted_by_phone': '555-0101',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Item.objects.count(), 1)
		self.assertEqual(Item.objects.first().status, 'pending')

	def test_seed_demo_data_creates_image_backed_dataset(self):
		call_command('seed_demo_data', reset=True)

		self.assertEqual(Item.objects.count(), 41)
		self.assertEqual(Item.objects.filter(status='pending').count(), 5)
		self.assertEqual(Item.objects.filter(status='approved').count(), 36)
		self.assertEqual(ClaimRequest.objects.count(), 2)
		self.assertFalse(Item.objects.filter(image__isnull=True).exists())
		self.assertFalse(Item.objects.filter(image='').exists())

		dates = list(Item.objects.values_list('date_found', flat=True))
		self.assertGreaterEqual(min(dates), date(2025, 12, 3))
		self.assertLessEqual(max(dates), date(2026, 3, 31))
		self.assertEqual(
			{(found_date.year, found_date.month) for found_date in dates},
			{(2025, 12), (2026, 1), (2026, 2), (2026, 3)},
		)
		self.assertTrue(Item.objects.filter(title='AirPods').exists())
		self.assertTrue(Item.objects.filter(title='Black Wallet', status='pending').exists())

	def test_found_items_only_shows_approved_or_claimed(self):
		Item.objects.create(
			title='Approved Backpack',
			category='school',
			description='Blue backpack',
			location_found='Library',
			date_found=date(2026, 3, 16),
			submitted_by_name='Sam',
			submitted_by_email='sam@example.com',
			status='approved',
		)
		Item.objects.create(
			title='Pending Phone',
			category='electronics',
			description='Locked phone',
			location_found='Cafeteria',
			date_found=date(2026, 3, 16),
			submitted_by_name='Pat',
			submitted_by_email='pat@example.com',
			status='pending',
		)

		response = self.client.get(reverse('found_items'))
		self.assertContains(response, 'Approved Backpack')
		self.assertNotContains(response, 'Pending Phone')

	def test_claim_submission_creates_pending_claim(self):
		item = Item.objects.create(
			title='Calculator',
			category='school',
			description='Graphing calculator',
			location_found='Room 202',
			date_found=date(2026, 3, 15),
			submitted_by_name='Lee',
			submitted_by_email='lee@example.com',
			status='approved',
		)

		response = self.client.post(
			reverse('claim_item', args=[item.id]),
			{
				'claimant_name': 'Jordan',
				'claimant_email': 'jordan@example.com',
				'claimant_phone': '555-0199',
				'proof_of_ownership': 'Name sticker and scratched corner.',
				'additional_message': 'Lost after math club.',
			},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(ClaimRequest.objects.count(), 1)
		self.assertEqual(ClaimRequest.objects.first().status, 'pending')

	def test_staff_can_approve_claim_and_item_becomes_claimed(self):
		item = Item.objects.create(
			title='Jacket',
			category='clothing',
			description='Black jacket',
			location_found='Auditorium',
			date_found=date(2026, 3, 14),
			submitted_by_name='Chris',
			submitted_by_email='chris@example.com',
			status='approved',
		)
		claim = ClaimRequest.objects.create(
			item=item,
			claimant_name='Jamie',
			claimant_email='jamie@example.com',
			proof_of_ownership='Inside label has my initials.',
		)

		self.client.login(username='staff1', password='testpass123')
		response = self.client.post(
			reverse('moderate_claim', args=[claim.id]),
			{'action': 'approve'},
			follow=True,
		)
		self.assertEqual(response.status_code, 200)

		claim.refresh_from_db()
		item.refresh_from_db()
		self.assertEqual(claim.status, 'approved')
		self.assertEqual(item.status, 'claimed')

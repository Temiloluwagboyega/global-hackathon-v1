from django.test import TestCase
from django.test import Client
from django.urls import reverse
import json

class WelcomeModalTestCase(TestCase):
	def setUp(self):
		self.client = Client()
	
	def test_check_welcome_modal_not_viewed(self):
		"""Test checking welcome modal status for new IP"""
		response = self.client.get('/api/welcome/check/')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertFalse(data['has_viewed'])
		self.assertIsNotNone(data['ip_address'])
	
	def test_mark_welcome_modal_viewed(self):
		"""Test marking welcome modal as viewed"""
		response = self.client.post('/api/welcome/mark-viewed/')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertTrue(data['success'])
		self.assertIsNotNone(data['viewed_at'])
	
	def test_welcome_modal_workflow(self):
		"""Test complete welcome modal workflow"""
		# First check - should not be viewed
		response = self.client.get('/api/welcome/check/')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertFalse(data['has_viewed'])
		
		# Mark as viewed
		response = self.client.post('/api/welcome/mark-viewed/')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertTrue(data['success'])
		
		# Check again - should now be viewed
		response = self.client.get('/api/welcome/check/')
		self.assertEqual(response.status_code, 200)
		data = json.loads(response.content)
		self.assertTrue(data['has_viewed'])
		self.assertIsNotNone(data['viewed_at'])

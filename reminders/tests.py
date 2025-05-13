from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta

class ReminderAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('reminder-list-create')

    def test_create_valid_reminder(self):
        future_time = datetime.now() + timedelta(hours=1)
        data = {
            "date": future_time.strftime("%Y-%m-%d"),
            "time": future_time.strftime("%H:%M"),
            "message": "Test Reminder",
            "reminder_method": "EMAIL"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Test Reminder")

    def test_create_reminder_in_past(self):
        past_time = datetime.now() - timedelta(hours=1)
        data = {
            "date": past_time.strftime("%Y-%m-%d"),
            "time": past_time.strftime("%H:%M"),
            "message": "This should fail",
            "reminder_method": "SMS"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reminder_with_invalid_method(self):
        future_time = datetime.now() + timedelta(hours=1)
        data = {
            "date": future_time.strftime("%Y-%m-%d"),
            "time": future_time.strftime("%H:%M"),
            "message": "Invalid method test",
            "reminder_method": "WHATSAPP"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

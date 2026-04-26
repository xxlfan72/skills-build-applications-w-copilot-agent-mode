from django.test import TestCase, Client
from .models import User, Team, Activity, Leaderboard, Workout

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_endpoints(self):
        endpoints = [
            '/api/users/',
            '/api/teams/',
            '/api/activities/',
            '/api/leaderboard/',
            '/api/workouts/',
        ]
        for ep in endpoints:
            response = self.client.get(ep)
            self.assertIn(response.status_code, [200, 403])  # 403 if auth required

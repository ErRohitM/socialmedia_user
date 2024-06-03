from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import AccuknoxUsers
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.search_url = reverse('user-search')
        
        # Create test user
        self.user = AccuknoxUsers.objects.create_user(email='test@example.com', password='testpassword', first_name='Test', last_name='User')
        
    def get_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)
        
    def test_user_signup(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_user_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_search_by_email(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.search_url, {'search': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'test@example.com')
        
    def test_user_search_by_name(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.search_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Test')

if __name__ == '__main__':
    import unittest
    unittest.main()

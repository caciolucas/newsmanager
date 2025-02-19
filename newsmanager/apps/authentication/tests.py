# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from authentication.models import User


class AuthTestCase(TestCase):
    fixtures = ["initial_data", "test_data"]

    def setUp(self):
        user = User.objects.filter(is_active=True).first()
        self.username = user.username
        self.password = "123"

    def test_token_obtain_pair_success(self):
        """
        Testa a obtenção do par de tokens (access e refresh) com credenciais válidas.
        """
        url = reverse("token_obtain_pair")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)

    def test_token_obtain_pair_invalid_credentials(self):
        """
        Testa que a obtenção de token falha quando as credenciais estão incorretas.
        """
        url = reverse("token_obtain_pair")
        data = {"username": self.username, "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        """
        Testa a geração de um novo token de acesso a partir de um refresh token válido.
        """
        obtain_url = reverse("token_obtain_pair")
        data = {"username": self.username, "password": self.password}
        obtain_response = self.client.post(obtain_url, data, format="json")
        self.assertEqual(obtain_response.status_code, status.HTTP_200_OK)
        refresh_token = obtain_response.data.get("refresh")
        self.assertIsNotNone(refresh_token)

        refresh_url = reverse("token_refresh")
        data = {"refresh": refresh_token}
        refresh_response = self.client.post(refresh_url, data, format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
        self.assertIsInstance(refresh_response.data["access"], str)

    def test_token_refresh_invalid_token(self):
        """
        Testa que o refresh falha quando o refresh token é inválido.
        """
        refresh_url = reverse("token_refresh")
        data = {"refresh": "invalidtoken"}
        response = self.client.post(refresh_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_missing_refresh(self):
        """
        Testa que o refresh falha quando o refresh token não é fornecido.
        """
        refresh_url = reverse("token_refresh")
        data = {}  # refresh token ausente
        response = self.client.post(refresh_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

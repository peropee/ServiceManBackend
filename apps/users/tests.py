import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration(client):
    url = reverse("users:register")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Testpass123!",
        "user_type": "CLIENT"
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(email="test@example.com").exists()
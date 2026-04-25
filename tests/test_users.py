import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
@pytest.mark.django_db
class TestUsers:
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("testpassword123")

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123"
        )

        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.check_password("adminpass123")

    def test_is_verified(self):
        user = User.objects.create_user(
            username="verify_user",
            email="verify@example.com",
            password="verify123"
        )
        assert not user.is_verified()

    def test_signup_redirects_to_verification(self, client):
        response = client.post(
            reverse("signup"),
            data={
                "username": "new_user",
                "first_name": "Іван",
                "last_name": "Петренко",
                "email": "new_user@example.com",
                "password": "password123",
                "phone_number": "+380991112233",
                "date_of_birth": "2000-01-01",
            },
        )

        assert response.status_code == 302
        assert response.url == reverse("verification_create")

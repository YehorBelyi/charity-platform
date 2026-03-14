import pytest
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user():
    User = get_user_model()

    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123"
    )

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.check_password("testpassword123")

# test
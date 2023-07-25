from django.contrib.auth.models import User


def create_test_user() -> None:
    User.objects.create_user(
        username="user",
        password="user12345",
        email="user1@example.com"
    )

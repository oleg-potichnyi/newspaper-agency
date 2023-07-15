import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from agency.models import Topic, Newspaper


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")

    def test_topic_str(self) -> None:
        topic = Topic.objects.create(name="test")
        self.assertEqual(str(topic), topic.name)

    def test_redactor_str(self) -> None:
        unique_id = uuid.uuid4().hex  # Generate a unique identifier
        username = f"test_{unique_id}"
        redactor = get_user_model().objects.create_user(
            username=username,
            password="test12345",
            first_name="Test first",
            last_name="Test last",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} {redactor.first_name} {redactor.last_name}",
        )

    def test_newspaper_str(self) -> None:
        topic = Topic.objects.create(name="test")
        newspaper = Newspaper.objects.create(title="test")
        newspaper.topic.set([topic])
        self.assertEqual(str(newspaper), newspaper.title)

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic

TOPIC_URL = reverse("agency:topic-list")


class PublicTopicTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(TOPIC_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTopicTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_topic(self) -> None:
        Topic.objects.create(name="name")
        response = self.client.get(TOPIC_URL)
        topic = Topic.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["topic_list"]),
            set(topic)
        )
        self.assertTemplateUsed(response, "agency/topic_list.html")

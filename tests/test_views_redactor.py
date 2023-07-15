from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from agency.models import Redactor

REDACTOR_URL = reverse("agency:redactor-list")


class PublicRedactorTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(REDACTOR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateRedactorTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_topic(self) -> None:
        Redactor.objects.create(username="username")
        response = self.client.get(REDACTOR_URL)
        redactor = Redactor.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context["redactor_list"]), set(redactor))
        self.assertTemplateUsed(response, "agency/redactor_list.html")

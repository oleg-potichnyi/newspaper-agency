import datetime

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from agency.models import Newspaper, Topic, Redactor

NEWSPAPER_URL = reverse("agency:newspaper-list")


class PublicNewspaperTests(TestCase):
    def test_login_required(self) -> None:
        res = self.client.get(NEWSPAPER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateNewspaperTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)

    def test_retrieve_topic(self) -> None:
        Newspaper.objects.create(title="title")
        response = self.client.get(NEWSPAPER_URL)
        newspaper = Newspaper.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["newspaper_list"]), set(newspaper)
        )
        self.assertTemplateUsed(response, "agency/newspaper_list.html")


class NewspaperCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("agency:newspaper-create")
        self.user = get_user_model().objects.create_user("test", "password123")
        self.topic = Topic.objects.create(name="topic_name")
        self.redactor = Redactor.objects.create(years_of_experience=228)

    def test_get_newspaper_success(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_newspaper_unauthorized(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_newspaper_success(self) -> None:
        data = {
            "title": "DW",
            "content": "abc",
            "published_date": datetime.datetime.now(),
            "topic": self.topic.pk,
            "publishers": self.redactor.pk,
            "redactors": [self.redactor.pk]
        }
        self.client.force_login(self.user)
        response: TemplateResponse = self.client.post(self.url, data)
        self.assertEqual(type(response), HttpResponseRedirect)
        self.assertTrue(Newspaper.objects.filter(title="DW").exists())
        self.assertRedirects(response, reverse("agency:newspaper-list"))

    def test_post_newspaper_unauthorized(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)


class NewspaperUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)
        self.newspaper = Newspaper.objects.create(title="First Name")
        self.url = reverse("agency:newspaper-update", args=[self.newspaper.pk])
        self.topic = Topic.objects.create(name="topic_name")
        self.redactor = Redactor.objects.create(years_of_experience=228)

    def test_get_newspaper_update_suc(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_newspaper_update_una(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_newspaper_update_suc(self) -> None:
        updated_newspaper_data = {
            "title": "DW",
            "content": "abc",
            "published_date": datetime.datetime.now(),
            "topic": self.topic.pk,
            "publishers": self.redactor.pk,
            "redactors": [self.redactor.pk]
        }
        response = self.client.post(self.url, data=updated_newspaper_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("agency:newspaper-list"))
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "DW")

    def test_post_newspaper_update_una(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)


class NewspaperDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)
        self.newspaper = Newspaper.objects.create(title="Newspaper to Delete")
        self.url = reverse("agency:newspaper-delete", args=[self.newspaper.pk])

    def test_get_newspaper_delete_suc(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_newspaper_update_una(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_newspaper_delete_suc(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("agency:newspaper-list"))
        self.assertFalse(
            Newspaper.objects.filter(pk=self.newspaper.pk).exists()
        )

    def test_post_newspaper_delete_una(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

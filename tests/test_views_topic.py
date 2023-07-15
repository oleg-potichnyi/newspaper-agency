from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse

from agency.models import Topic

TOPIC_URL = reverse("agency:topic-list")
NEWSPAPER_URL = reverse("agency:newspaper-list")


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
        self.assertEqual(set(response.context["topic_list"]), set(topic))
        self.assertTemplateUsed(response, "agency/topic_list.html")


class TopicCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.url = reverse("agency:topic-create")
        self.user = get_user_model().objects.create_user("test", "password123")

    def test_get_topic_success(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_topic_unauthorized(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_topic_success(self) -> None:
        data = {"name": "Politics"}
        self.client.force_login(self.user)
        response = self.client.post(self.url, data)
        self.assertEqual(type(response), HttpResponseRedirect)
        self.assertTrue(Topic.objects.filter(name="Politics").exists())
        self.assertRedirects(response, reverse("agency:topic-list"))

    def test_post_topic_unauthorized(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)


class TopicUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="First Name")
        self.url = reverse("agency:topic-update", args=[self.topic.pk])

    def test_get_topic_update_suc(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_topic_update_una(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_topic_update_suc(self) -> None:
        updated_data = {
            "name": "New Name",
        }
        response = self.client.post(self.url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("agency:topic-list"))
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "New Name")

    def test_post_topic_update_una(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)


class TopicDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test", "password123")
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="Topic to Delete")
        self.url = reverse("agency:topic-delete", args=[self.topic.pk])

    def test_get_topic_delete_suc(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(type(response), TemplateResponse)

    def test_get_topic_update_una(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_topic_delete_suc(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("agency:topic-list"))
        self.assertFalse(Topic.objects.filter(pk=self.topic.pk).exists())

    def test_post_topic_delete_una(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

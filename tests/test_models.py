# from unittest import TestCase
#
# from django.contrib.auth import get_user_model
#
# from agency.models import Topic, Newspaper
#
#
# class ModelsTests(TestCase):
#     def test_topic_str(self) -> None:
#         topic = Topic.objects.create(name="test")
#         self.assertEqual(str(topic), f"{topic.name}")
#
#     def test_redactor_str(self) -> None:
#         redactor = get_user_model().objects.create_user(
#             username="test",
#             password="test12345",
#             first_name="Test first",
#             last_name="Test last",
#         )
#         self.assertEqual(
#             str(redactor),
#             f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
#         )
#
#     def test_newspaper_str(self) -> None:
#         topic = Topic.objects.create(name="test")
#         newspaper = Newspaper.objects.create(title="test", topic=topic)
#         self.assertEqual(str(newspaper), newspaper.model)

from unittest import TestCase

from agency.forms import NewspaperSearchForm


class NewspaperSearchFormTests(TestCase):
    def test_newspaper_search_form(self) -> None:
        form_data = {"title": "Test title"}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Test title")
        model_field = form.fields["title"]
        self.assertEqual(model_field.label, "")
        self.assertEqual(model_field.required, False)
        self.assertEqual(
            model_field.widget.attrs.get("placeholder"), "Search by title.."
        )

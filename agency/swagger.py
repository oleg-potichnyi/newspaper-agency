from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API description",
        terms_of_service="https://your-terms-of-service-url.com/",
        contact=openapi.Contact(email="your-contact-email@example.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)

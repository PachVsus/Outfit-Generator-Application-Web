from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Import the home view from the wardrobe app
from wardrobe.views import home

# URL patterns for the project
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("app/", include("wardrobe.urls")),
    path("", home, name="home"),
]

# If the DEBUG setting is True, serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

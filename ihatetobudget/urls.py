from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sheets/", include("sheets.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Budget dashboard routes are under the sheets/ prefix (see include("sheets.urls")).
# For backwards-compatibility, mirror them at the root.
from sheets.views import budget_dashboard
urlpatterns += [
    path("budget/", budget_dashboard, name="budget_dashboard"),
    path("budget/<int:year>/<int:month>/", budget_dashboard, name="budget_dashboard_monthly"),
]

# Serve uploaded media files in development.
# This is required for `{{ e.receipt.url }}` downloads to work when DEBUG=True.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


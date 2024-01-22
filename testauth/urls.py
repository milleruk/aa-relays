# Django
# Alliance Auth
from django.urls import include, path

from allianceauth import urls

urlpatterns = [
    # Alliance Auth URLs
    path("", include(urls)),
]

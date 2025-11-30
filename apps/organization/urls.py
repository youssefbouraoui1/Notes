from django.urls import path
from .views import ListCreateOrganization, UpdateDeleteOrganization, invite_to_organization

urlpatterns = [
    path("", ListCreateOrganization.as_view()),
    path("<uuid:id>/", UpdateDeleteOrganization.as_view()),
    path("invite/", invite_to_organization),
]

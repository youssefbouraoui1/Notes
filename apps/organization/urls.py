from django.urls import path
from .views import ListCreateOrganization, UpdateDeleteOrganization, invite_to_organization, UpdateDeleteOrganizationBySlug, ListOrganizationMembers, RemoveMemberFromOrganization

urlpatterns = [
    path("", ListCreateOrganization.as_view()),
    path("<uuid:id>/", UpdateDeleteOrganization.as_view()),
    path("<slug:slug>/", UpdateDeleteOrganizationBySlug.as_view()),
    path("<slug:slug>/members/", ListOrganizationMembers.as_view(), name="organization-members"),
    path("<slug:slug>/members/<uuid:id>/",RemoveMemberFromOrganization.as_view()),
    path("invite/", invite_to_organization),
]

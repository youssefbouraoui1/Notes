from django.urls import path
from .views import ListCreateProject, GetProjectByOrganization

urlpatterns = [
    path("",ListCreateProject.as_view()),
    path("<uuid:organization_id>", GetProjectByOrganization.as_view())
]
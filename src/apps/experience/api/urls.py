from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.experience.api.views import (
    ExperienceCRUDApiView, ProjectCreateReadApiView,
    ProjectUpdateDeleteApiView, ReferencePeopleCRUDApiView,
    PersonalProjectCRUDApiView, ProjectAssetsDeleteApiView,
    PersonalProjectAssetsDeleteApiView, BlogCRUDApiView
)

router = DefaultRouter()
router.register("experience", ExperienceCRUDApiView, "experience")
router.register("reference", ReferencePeopleCRUDApiView, "reference")
router.register("personal_project", PersonalProjectCRUDApiView, "personal_project")
router.register("blog", BlogCRUDApiView, "blog")

app_name = "experience"

urlpatterns = [
    path(
        'project/<slug:slug>/',
        ProjectCreateReadApiView.as_view(),
        name='project_CR'
    ),
    path(
        'project/<slug:slug>/<int:pk>/',
        ProjectUpdateDeleteApiView.as_view(),
        name='project_UD'
    ),
    path(
        'project/asset/<slug:slug>/<int:pk>/',
        ProjectAssetsDeleteApiView.as_view(),
        name='project_delete_asset'
    ),
    path(
        'personal_project/asset/<int:pk>/',
        PersonalProjectAssetsDeleteApiView.as_view(),
        name='personal_project_delete_asset'
    ),
]

urlpatterns += router.urls

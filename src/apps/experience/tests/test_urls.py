from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.experience.api.views import (
    ProjectUpdateDeleteApiView, ProjectAssetsDeleteApiView,
    ReferencePeopleCRUDApiView, PersonalProjectCRUDApiView,
    PersonalProjectAssetsDeleteApiView, BlogCRUDApiView,
    ExperienceCRUDApiView, ProjectCreateReadApiView,

)


class ExperienceUrlsApiTest(SimpleTestCase):

    def test_experience_url(self):
        path = resolve("/api/v1/experience/")
        self.assertNotEqual(
            path.func.__name__,
            BlogCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            ExperienceCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_project_CR_url(self):
        path = reverse('experience:project_CR', args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            ProjectCreateReadApiView,
        )

    def test_project_UD_url(self):
        path = reverse('experience:project_UD', args=['slug', 1])
        self.assertEqual(
            resolve(path).func.view_class,
            ProjectUpdateDeleteApiView,
        )

    def test_project_asset_delete_url(self):
        path = reverse('experience:project_delete_asset', args=['slug', 1])
        self.assertNotEqual(
            resolve(path).func.view_class,
            ProjectUpdateDeleteApiView,
        )
        self.assertEqual(
            resolve(path).func.view_class,
            ProjectAssetsDeleteApiView,
        )

    def test_reference_url(self):
        path = resolve("/api/v1/reference/")
        self.assertNotEqual(
            path.func.__name__,
            ExperienceCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            ReferencePeopleCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_personal_project_url(self):
        path = resolve("/api/v1/personal_project/")
        self.assertNotEqual(
            path.func.__name__,
            ExperienceCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            PersonalProjectCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_personal_project_asset_delete_url(self):
        path = reverse("experience:personal_project_delete_asset", args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            PersonalProjectAssetsDeleteApiView
        )

    def test_blog_url(self):
        path = resolve("/api/v1/blog/")
        self.assertNotEqual(
            path.func.__name__,
            PersonalProjectCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            BlogCRUDApiView.as_view({'get': 'list'}).__name__,
        )

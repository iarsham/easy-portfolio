from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.portfolio.api.views import (
    AboutMeGetUpdateApiView, AboutMeDeleteProfileApiView, SendContactMeApiView,
    EducationGetUpdateApiView, SkillCRUDApiView, SkillDeleteCertificateApiView,
    AchievementCRUDApiView, AchievementDeleteCertificateApiView,
    LanguageCRUDApiView, LanguageDeleteCertificateApiView,
)


class PortfolioUrlsApiTest(SimpleTestCase):

    def test_about_me_url(self):
        path = reverse("portfolio:about_me")
        self.assertEqual(
            resolve(path).func.view_class, AboutMeGetUpdateApiView
        )

    def test_education_url(self):
        path = reverse("portfolio:education")
        self.assertEqual(
            resolve(path).func.view_class, EducationGetUpdateApiView
        )

    def test_about_me_profile_delete_url(self):
        path = reverse("portfolio:aboutme_delete_profile", args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            AboutMeDeleteProfileApiView
        )

    def test_skill_url(self):
        path = resolve("/api/v1/skill/")
        self.assertEqual(
            path.func.__name__,
            SkillCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_skill_certificate_delete_url(self):
        path = reverse("portfolio:skill_delete_certificate", args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            SkillDeleteCertificateApiView
        )

    def test_language_url(self):
        path = resolve("/api/v1/language/")
        self.assertNotEqual(
            path.func.__name__,
            SkillCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            LanguageCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_language_certificate_delete_url(self):
        path = reverse("portfolio:language_delete_certificate", args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            LanguageDeleteCertificateApiView
        )

    def test_achievement_url(self):
        path = resolve("/api/v1/achievement/")
        self.assertNotEqual(
            path.func.__name__,
            LanguageCRUDApiView.as_view({'get': 'list'}).__name__,
        )
        self.assertEqual(
            path.func.__name__,
            AchievementCRUDApiView.as_view({'get': 'list'}).__name__,
        )

    def test_achievement_certificate_delete_url(self):
        path = reverse("portfolio:achievement_delete_certificate", args=[1])
        self.assertEqual(
            resolve(path).func.view_class,
            AchievementDeleteCertificateApiView
        )

    def test_contact_me_url(self):
        path = reverse("portfolio:contact_me")
        self.assertEqual(
            resolve(path).func.view_class,
            SendContactMeApiView
        )

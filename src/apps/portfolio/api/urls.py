from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.portfolio.api.views import (
    AboutMeGetUpdateApiView, AboutMeDeleteProfileApiView,
    EducationGetUpdateApiView, SkillCRUDApiView, SkillDeleteCertificateApiView,
    LanguageCRUDApiView, LanguageDeleteCertificateApiView,
    AchievementCRUDApiView, AchievementDeleteCertificateApiView,
    EmploymentChoicesApiView, ProficiencyChoicesApiView
)

router = DefaultRouter()
router.register("skill", SkillCRUDApiView, "skill")
router.register("language", LanguageCRUDApiView, "language")
router.register("achievement", AchievementCRUDApiView, "achievement")

app_name = 'portfolio'

urlpatterns = [
    path(
        'aboutme/',
        AboutMeGetUpdateApiView.as_view(),
        name='about_me'
    ),
    path(
        'education/',
        EducationGetUpdateApiView.as_view(),
        name='education'
    ),
    path(
        'aboutme/profile/<int:pk>/',
        AboutMeDeleteProfileApiView.as_view(),
        name='aboutme_delete_profile'
    ),
    path(
        'skill/certificate/<int:pk>/',
        SkillDeleteCertificateApiView.as_view(),
        name='skill_delete_certificate'
    ),
    path(
        'language/certificate/<int:pk>/',
        LanguageDeleteCertificateApiView.as_view(),
        name='language_delete_certificate'
    ),
    path(
        'achievement/certificate/<int:pk>/',
        AchievementDeleteCertificateApiView.as_view(),
        name='achievement_delete_certificate'
    ),
    path('proficiency/', ProficiencyChoicesApiView.as_view()),
    path('employment/', EmploymentChoicesApiView.as_view())

]
urlpatterns += router.urls

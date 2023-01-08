from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.portfolio.api.views import (
    AboutMeGetUpdateApiView, AboutMeDeleteProfileApiView,
    AboutMeUpdateResumeApiView, AboutMeUpdateProfileApiView,
    EducationGetUpdateApiView, SkillCRUDApiView, SkillCreateCertificateApiView,
    SkillDeleteCertificateApiView, LanguageCRUDApiView,
    LanguageDeleteCertificateApiView, AchievementCRUDApiView,
    AchievementDeleteCertificateApiView, EmploymentChoicesApiView,
    ProficiencyChoicesApiView, SendContactMeApiView,
    LanguageCertificateCreateApiView, AchievementCertificateCreateApiView
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
        'aboutme/resume/',
        AboutMeUpdateResumeApiView.as_view(),
        name='about_me_resume'
    ), path(
        'aboutme/profile/',
        AboutMeUpdateProfileApiView.as_view(),
        name='aboutme_update_profile'
    ),
    path(
        'aboutme/profile/<int:pk>/',
        AboutMeDeleteProfileApiView.as_view(),
        name='aboutme_delete_profile'
    ),
    path(
        'education/',
        EducationGetUpdateApiView.as_view(),
        name='education'
    ),
    path(
        'skill/certificate/create/<int:pk>/',
        SkillCreateCertificateApiView.as_view(),
        name='skill_create_certificate'
    ),
    path(
        'skill/certificate/<int:pk>/',
        SkillDeleteCertificateApiView.as_view(),
        name='skill_delete_certificate'
    ),
    path(
        'language/certificate/create/<int:pk>/',
        LanguageCertificateCreateApiView.as_view(),
        name='language_create_certificate'
    ),
    path(
        'language/certificate/<int:pk>/',
        LanguageDeleteCertificateApiView.as_view(),
        name='language_delete_certificate'
    ),
    path(
        'achievement/certificate/create/<int:pk>/',
        AchievementCertificateCreateApiView.as_view(),
        name='achievement_create_certificate'
    ),
    path(
        'achievement/certificate/<int:pk>/',
        AchievementDeleteCertificateApiView.as_view(),
        name='achievement_delete_certificate'
    ),
    path('proficiency/', ProficiencyChoicesApiView.as_view()),
    path('employment/', EmploymentChoicesApiView.as_view()),
    path('contactme/', SendContactMeApiView.as_view(), name='contact_me')

]
urlpatterns += router.urls

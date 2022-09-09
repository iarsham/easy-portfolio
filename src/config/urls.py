from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from config.settings import base
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

schema_view = get_schema_view(
    openapi.Info(
        title="Easy Portfolio API",
        default_version='v1',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aqaarsham@gmail.com"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.api.urls', namespace="users_v1")),
    path('api/v1/', include('apps.portfolio.api.urls', namespace="portfolio_v1")),
    path('api/v1/', include('apps.experience.api.urls', namespace="experience_v1")),
    path('api/v1/', include('config.dj_urls')),
    # Password Reset
    path(
        'api/v1/password_reset/',
        PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'api/v1/password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    # Verification Email
    path(
        'api/v1/resend_verification_email/',
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email"
    ),
    path(
        'api/v1/email_verification_sent/',
        ConfirmEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    path(
        'api/v1/confirm-email/<str:key>/',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),

    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
            ),
]

if settings.INTERNAL_IPS:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(base.STATIC_URL, document_root=base.STATIC_ROOT)
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

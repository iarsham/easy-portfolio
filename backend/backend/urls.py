from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls', namespace='user')),

    path('api/password_reset/',
         PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('api/resend_verification_email/',
         ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('api/email_verification_sent/',
         ConfirmEmailView.as_view(), name='account_email_verification_sent'),
    path('api/confirm-email/<str:key>/',
         VerifyEmailView.as_view(), name='account_confirm_email'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import Response, status, APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from apps.portfolio.constants import PROFICIENCY_STATUS, EMPLOYMENT_STATUS
from apps.extensions.inheritances import BaseViewSetMixin
from apps.portfolio.permissions import (
    IsLanguageCertificateOwner, IsAchievementCertificateOwner,
    IsSkillCertificateOwner
)
from apps.portfolio.models import (
    AboutMe, AboutMeProfile, Education, Skill,
    SkillCertificate, Language, LanguageCertificate,
    Achievement, AchievementCertificate, ContactMe
)
from apps.portfolio.api.serializers import (
    AboutMeSerializer, LanguageSerializer, EducationSerializer,
    SkillSerializer, AchievementSerializer, ContactMeSerializer
)
from apps.portfolio.tasks import send_contact_me_mail


class AboutMeGetUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = AboutMeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'put']

    def get_object(self):
        return get_object_or_404(AboutMe, user=self.request.user)


class AboutMeDeleteProfileApiView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_object_or_404(
            AboutMeProfile,
            about_me__user=self.request.user,
            id=self.kwargs['pk']
        )
        return obj


class EducationGetUpdateApiView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EducationSerializer
    http_method_names = ['get', 'put']

    def get_object(self):
        obj_about_me = get_object_or_404(AboutMe, user=self.request.user)
        return get_object_or_404(Education, about_me=obj_about_me)


class SkillCRUDApiView(BaseViewSetMixin):
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Skill.objects.filter(about_me__user=self.request.user)

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj_about_me = get_object_or_404(AboutMe, user=self.request.user)
        if self.request.method == "POST":
            return obj_about_me
        return get_object_or_404(Skill, about_me=obj_about_me, id=pk)


class SkillDeleteCertificateApiView(generics.DestroyAPIView):
    permission_classes = (IsSkillCertificateOwner,)

    def get_object(self):
        try:
            obj = SkillCertificate.objects.select_related(
                "skill",
                "skill__about_me",
                "skill__about_me__user"
            ).get(id=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(
                _("with this id no certificate found")
            )


class LanguageCRUDApiView(BaseViewSetMixin):
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Language.objects.filter(about_me__user=self.request.user)

    def get_object(self):
        obj_about_me = get_object_or_404(AboutMe, user=self.request.user)
        pk = self.kwargs.get('pk')
        if self.request.method == "POST":
            return obj_about_me
        return get_object_or_404(Language, about_me=obj_about_me, id=pk)


class LanguageDeleteCertificateApiView(generics.DestroyAPIView):
    permission_classes = (IsLanguageCertificateOwner,)

    def get_object(self):
        try:
            obj = LanguageCertificate.objects.select_related(
                "language",
                "language__about_me",
                "language__about_me__user"
            ).get(id=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(
                _("with this id no certificate found")
            )


class AchievementCRUDApiView(BaseViewSetMixin):
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return Achievement.objects.filter(about_me__user=self.request.user)

    def get_object(self):
        obj_about_me = get_object_or_404(AboutMe, user=self.request.user)
        pk = self.kwargs.get('pk')
        if self.request.method == "POST":
            return obj_about_me
        return get_object_or_404(Achievement, about_me=obj_about_me, id=pk)


class AchievementDeleteCertificateApiView(generics.DestroyAPIView):
    permission_classes = (IsAchievementCertificateOwner,)

    def get_object(self):
        try:
            obj = AchievementCertificate.objects.select_related(
                "achievement",
                "achievement__about_me",
                "achievement__about_me__user"
            ).get(id=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise NotFound(
                _("with this id no certificate found")
            )


class ProficiencyChoicesApiView(APIView):
    def get(self, request, *args, **kwargs):
        choices = [choice[0] for choice in PROFICIENCY_STATUS]
        return Response({"response": choices}, status=status.HTTP_200_OK)


class EmploymentChoicesApiView(APIView):
    def get(self, request, *args, **kwargs):
        choices = [choice[0] for choice in EMPLOYMENT_STATUS]
        return Response({"response": choices}, status=status.HTTP_200_OK)


class SendContactMeApiView(generics.CreateAPIView):
    queryset = ContactMe.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ContactMeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            send_contact_me_mail.delay(
                message=data['message'], email=data['email'],
                user_email=request.user.email,
                name=data['name'], subject=data['subject'],
            )
            return Response(
                {"response": "message was sent!"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

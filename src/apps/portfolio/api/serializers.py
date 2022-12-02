from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.portfolio.models import (
    AboutMe, Education, Skill, SkillCertificate,
    AboutMeProfile, Language, LanguageCertificate,
    Achievement, AchievementCertificate, ContactMe
)


class AboutMeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMeProfile
        fields = ("id", "image")


class AboutMeUpdateResumeSerializer(serializers.ModelSerializer):
    resume = serializers.FileField()

    class Meta:
        model = AboutMe
        fields = ("resume",)


class AboutMeUpdateProfileSerializer(serializers.Serializer):
    profile = serializers.FileField()


class AboutMeSerializer(serializers.ModelSerializer):
    profile_images = serializers.SerializerMethodField('get_images')
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = AboutMe
        exclude = (
            "id", "created",
            "user", "updated",
        )

    def get_images(self, obj):
        return AboutMeProfileSerializer(
            instance=obj.aboutme_profile.all(),
            many=True,
            context={"request": self.context['request']}
        ).data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('id', 'about_me')
        extra_kwargs = {'start_time': {'required': True}}

    def validate(self, attrs):
        finish_time = attrs.get('finish_time', None)
        if finish_time is not None and finish_time <= attrs['start_time']:
            raise ValidationError(
                _("The end date cannot be less than the start date")
            )
        return attrs

    def to_representation(self, instance):
        context = super().to_representation(instance)
        if instance.start_time is not None and not instance.finish_time:
            context['status'] = "until now"
            return context
        elif instance.start_time and instance.finish_time:
            context['status'] = "finished"
            return context
        else:
            return context


class SkillCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCertificate
        fields = ("id", "certificate")


class SkillSerializer(serializers.ModelSerializer):
    certificates = serializers.SerializerMethodField('get_assets')

    class Meta:
        model = Skill
        fields = ("id", "name", "certificates")

    def get_assets(self, obj):
        return SkillCertificateSerializer(
            instance=obj.skill_certificate.all(),
            many=True,
            context={"request": self.context['request']}
        ).data

    def validate_name(self, data):
        request = self.context['request']
        if request.method == "POST" and Skill.objects.filter(
                about_me__user=request.user,
                name__icontains=data
        ).exists():
            raise ValidationError(_("This skill already exists"))
        return data


class SkillCreateCertificateSerializer(serializers.Serializer):
    certificate = serializers.FileField()


class LanguageCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageCertificate
        fields = ("id", "certificate")


class LanguageSerializer(serializers.ModelSerializer):
    certificates = serializers.SerializerMethodField('get_assets')

    class Meta:
        model = Language
        fields = ("id", "name", "proficiency", "certificates")

    def validate_name(self, data):
        request = self.context['request']
        if request.method == "POST" and Language.objects.filter(
                about_me__user=request.user,
                name__icontains=data
        ).exists():
            raise ValidationError(_("This language already exists"))
        return data

    def get_assets(self, obj):
        return LanguageCertificateSerializer(
            instance=obj.language_certificate.all(),
            many=True,
            context={"request": self.context['request']}
        ).data

class LanguageCertificateCreateSerializer(serializers.Serializer):
    certificate = serializers.FileField()


class AchievementCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementCertificate
        fields = ("id", "certificate")


class AchievementSerializer(serializers.ModelSerializer):
    certificates = serializers.SerializerMethodField('get_assets')

    class Meta:
        model = Achievement
        fields = ("id", "title", "description", "certificates")

    def get_assets(self, obj):
        return AchievementCertificateSerializer(
            instance=obj.achievement_certificate.all(),
            many=True,
            context={"request": self.context['request']}
        ).data

    def validate_title(self, data):
        request = self.context['request']
        if request.method == "POST" and Achievement.objects.filter(
                about_me__user=request.user,
                title__icontains=data
        ).exists():
            raise ValidationError(_("This achievement already exists"))
        return data


class AchievementCertificateCreateSerializer(serializers.Serializer):
    certificate = serializers.FileField()


class ContactMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMe
        exclude = ('user', 'created', 'updated')

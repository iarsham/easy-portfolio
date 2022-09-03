from rest_framework.permissions import BasePermission


class IsSkillCertificateOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.skill.about_me.user == request.user
        )


class IsLanguageCertificateOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.language.about_me.user == request.user
        )


class IsAchievementCertificateOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.achievement.about_me.user == request.user
        )

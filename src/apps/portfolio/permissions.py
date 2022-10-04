from rest_framework.permissions import IsAuthenticated


class IsSkillCertificateOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.skill.about_me.user == request.user
        )


class IsLanguageCertificateOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.language.about_me.user == request.user
        )


class IsAchievementCertificateOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.achievement.about_me.user == request.user
        )

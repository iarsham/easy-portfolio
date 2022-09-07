from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedAndOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.user == request.user
        )


class IsProjectOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.experience.user == request.user
        )


class IsProjectAssetsOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.project.experience.user == request.user
        )


class IsPersonalProjectOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.personal_project.user == request.user
        )

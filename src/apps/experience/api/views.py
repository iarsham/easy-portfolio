from django.shortcuts import get_object_or_404
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from apps.portfolio.api.views import BaseViewSetMixin
from apps.experience.permissions import (
    IsAuthenticatedAndOwner, IsProjectOwner,
    IsProjectAssetsOwner, IsPersonalProjectOwner,
)
from apps.experience.models import (
    Experience, Project, ProjectAssets,
    PersonalProject, PersonalProjectAssets,
    ReferencePeople
)
from apps.experience.api.serializers import (
    ExperienceSerializer, ProjectSerializer,
    ReferencePeopleSerializer, PersonalProjectSerializer
)


class BaseUpdateDeleteMixin(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExperienceCRUDApiView(BaseViewSetMixin):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.filter(
            user=self.request.user
        ).order_by('-start_date')

    def get_object(self):
        obj = get_object_or_404(Experience, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectCreateReadApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            experience__user=self.request.user,
            experience__slug=self.kwargs['slug']
        )

    def perform_create(self, serializer):
        exp_obj = get_object_or_404(Experience, slug=self.kwargs['slug'])
        if exp_obj.user != self.request.user:
            raise PermissionDenied("You are not this experience object owner")
        return serializer.save(experience=exp_obj)


class ProjectUpdateDeleteApiView(BaseUpdateDeleteMixin):
    permission_classes = (IsProjectOwner,)
    serializer_class = ProjectSerializer

    def get_object(self):
        obj = get_object_or_404(
            Project,
            experience__slug=self.kwargs['slug'],
            id=self.kwargs['pk']
        )
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectAssetsDeleteApiView(generics.DestroyAPIView):
    permission_classes = (IsProjectAssetsOwner,)

    def get_object(self):
        obj = get_object_or_404(
            ProjectAssets,
            project__experience__slug=self.kwargs['slug'],
            id=self.kwargs['pk']
        )
        self.check_object_permissions(self.request, obj)
        return obj


class ReferencePeopleCRUDApiView(BaseViewSetMixin):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = ReferencePeopleSerializer

    def get_queryset(self):
        return ReferencePeople.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(ReferencePeople, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalProjectCRUDApiView(BaseViewSetMixin):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = PersonalProjectSerializer

    def get_queryset(self):
        return PersonalProject.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(PersonalProject, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalProjectAssetsDeleteApiView(generics.DestroyAPIView):
    permission_classes = (IsPersonalProjectOwner,)

    def get_object(self):
        obj = get_object_or_404(
            PersonalProjectAssets,
            id=self.kwargs['pk']
        )
        self.check_object_permissions(self.request, obj)
        return obj

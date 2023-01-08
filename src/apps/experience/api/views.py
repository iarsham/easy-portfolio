from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from apps.extensions.inheritances import (
    BaseViewSetMixin, BaseUpdateDeleteMixin, BlogPagination
)
from apps.experience.permissions import (
    IsAuthenticatedAndOwner, IsProjectOwner,
    IsProjectAssetsOwner, IsPersonalProjectOwner,
)
from apps.experience.models import (
    Experience, Project, ProjectAssets,
    PersonalProject, PersonalProjectAssets,
    ReferencePeople, Blog
)
from apps.experience.api.serializers import (
    ExperienceSerializer, ProjectSerializer, BlogSerializer,
    ReferencePeopleSerializer, PersonalProjectSerializer,
    ProjectAssetCreateSerializer, ReferencePeopleImageSerializer,
    PersonalProjectAssetSerializer
)


class ExperienceCRUDApiView(BaseViewSetMixin):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.filter(
            user=self.request.user
        ).order_by('-start_date')

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


class ProjectAssetCreateApiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectAssetCreateSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self):
        obj = get_object_or_404(
            Project,
            experience__user=self.request.user,
            experience__slug=self.kwargs['slug'],
            id=self.kwargs['pk']
        )
        return obj

    def create(self, request, *args, **kwargs):
        if request.FILES and request.FILES.get('asset'):
            assets_obj_list = []
            for file in request.FILES.getlist('asset'):
                assets_obj_list.append(
                    ProjectAssets(project=self.get_object(), file=file))
            ProjectAssets.objects.bulk_create(assets_obj_list)
        else:
            raise ValidationError(
                detail={"asset": "No file was submitted."},
                code=status.HTTP_400_BAD_REQUEST
            )
        return Response({"response": "files added"}, status.HTTP_200_OK)


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReferencePeopleImageApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = ReferencePeopleImageSerializer
    parser_classes = (FormParser, MultiPartParser)
    http_method_names = ['put']

    def get_object(self):
        return get_object_or_404(
            ReferencePeople,
            user=self.request.user,
            id=self.kwargs['pk']
        )


class PersonalProjectCRUDApiView(BaseViewSetMixin):
    permission_classes = (IsAuthenticatedAndOwner,)
    serializer_class = PersonalProjectSerializer

    def get_queryset(self):
        return PersonalProject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PersonalProjectAssetCreateApiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PersonalProjectAssetSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get_object(self):
        return get_object_or_404(
            PersonalProject,
            user=self.request.user,
            id=self.kwargs['pk']
        )

    def create(self, request, *args, **kwargs):
        if request.FILES and request.FILES.get('asset'):
            assets_obj_list = []
            for file in request.FILES.getlist('asset'):
                assets_obj_list.append(
                    PersonalProjectAssets(
                        personal_project=self.get_object(),
                        file=file
                    )
                )
            PersonalProjectAssets.objects.bulk_create(assets_obj_list)
        else:
            raise ValidationError(
                detail={"asset": "No file was submitted."},
                code=status.HTTP_400_BAD_REQUEST
            )
        return Response({"response": "files added"}, status.HTTP_200_OK)


class PersonalProjectAssetsDeleteApiView(generics.DestroyAPIView):
    queryset = PersonalProjectAssets.objects.all()
    permission_classes = (IsPersonalProjectOwner,)


class BlogCRUDApiView(BaseViewSetMixin):
    serializer_class = BlogSerializer
    pagination_class = BlogPagination
    permission_classes = (IsAuthenticatedAndOwner,)

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

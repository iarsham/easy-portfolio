from rest_framework import mixins, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet


class BaseViewSetMixin(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        serializer.save(about_me=self.get_object())


class BaseUpdateDeleteMixin(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BlogPagination(PageNumberPagination):
    page_size = 3

from promises.models import Promise
from promises.serializers import PromiseSerializer, UserSerializer
from promises.serializers import PromiseSerializerWithoutUser
from promises.serializers import UserAllSerializer
from promises.permissions import IsRelated
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response


class PromiseList(generics.ListCreateAPIView):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # automatically add user info when creating promise
    # override
    def perform_create(self, serializer):
        # user 1 is the one who made promise
        serializer.save(user1=self.request.user)

    # check if sicneWhen < tilWhen and user1.id != user2.id
    # override
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sinceWhen = serializer.validated_data["sinceWhen"]
        tilWhen = serializer.validated_data["tilWhen"]
        user1_id = request.user.id
        user2_id = serializer.validated_data["user2"].id

        # custom invalid data
        if sinceWhen >= tilWhen or user1_id == user2_id :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PromiseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializerWithoutUser
    permission_classes = (permissions.IsAuthenticated, IsRelated,)

    # check if sicneWhen < tilWhen
    # override
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        sinceWhen = serializer.validated_data["sinceWhen"]
        tilWhen = serializer.validated_data["tilWhen"]

        # custom invalid data
        if sinceWhen >= tilWhen :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAllList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer


class UserAllDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllSerializer

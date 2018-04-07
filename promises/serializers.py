from rest_framework import serializers
from promises.models import Promise
from django.contrib.auth.models import User


class PromiseSerializer(serializers.ModelSerializer):
    user1 = serializers.ReadOnlyField(source="user1.id")
    #  user1 = serializers.ReadOnlyField(source="user1.id")

    class Meta:
        model = Promise
        fields = "__all__"


class PromiseSerializerWithoutUser(serializers.ModelSerializer):
    user1 = serializers.ReadOnlyField(source="user1.id")
    user2 = serializers.ReadOnlyField(source="user2.id")

    class Meta:
        model = Promise
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "promises_as_inviter", "promises_as_invitee")


class UserAllSerializer(serializers.ModelSerializer):
    whole_promises = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "whole_promises")

    # obj is User
    def get_whole_promises(self, obj):
        inviter = [promise.id for promise in obj.promises_as_inviter.all()]
        invitee = [promise.id for promise in obj.promises_as_invitee.all()]

        return inviter + invitee

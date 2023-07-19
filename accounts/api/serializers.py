from django.contrib.auth.backends import get_user_model

from djoser.serializers import UserSerializer, UserCreateSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (*UserCreateSerializer.Meta.fields, 'role')


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (*UserSerializer.Meta.fields, 'role')
        read_only_fields = (*UserSerializer.Meta.read_only_fields, )

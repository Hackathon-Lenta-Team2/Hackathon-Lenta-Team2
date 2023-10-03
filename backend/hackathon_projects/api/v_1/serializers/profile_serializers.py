from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Отображение информации о пользователе."""

    class Meta:
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name',
        )
        model = User

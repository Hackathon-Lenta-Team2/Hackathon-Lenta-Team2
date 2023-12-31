from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v_1.serializers.profile_serializers import ProfileSerializer


@extend_schema(
    operation_id="Get User profile",
    tags=("User Profile",),
    description="Получение информации о пользователе.",
    responses=ProfileSerializer,
)
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def profile_view(request):
    """Функция отображения информации о пользователе."""
    user = request.user
    serializer = ProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

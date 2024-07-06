
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from .permissions import IsSuperAdmin

class MySuperAdminView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request, format=None):
        data = {"message": "Hello, Superadmin!"}
        return Response(data, status=status.HTTP_200_OK)

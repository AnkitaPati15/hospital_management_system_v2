from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer


class DepartmentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        departments = Department.objects.all()

        serializer = DepartmentSerializer(
            departments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'admin':
            return Response(
                {
                    'error': 'Only admin can create department'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DepartmentSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
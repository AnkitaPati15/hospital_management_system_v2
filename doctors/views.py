from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        doctors = Doctor.objects.all()

        serializer = DoctorSerializer(
            doctors,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'admin':
            return Response(
                {
                    'error': 'Only admin can create doctors'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DoctorSerializer(
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


class DoctorDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return Doctor.objects.get(pk=pk)

    def get(self, request, pk):

        doctor = self.get_object(pk)

        serializer = DoctorSerializer(doctor)

        return Response(serializer.data)
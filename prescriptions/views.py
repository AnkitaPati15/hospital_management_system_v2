from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Prescription
from .serializers import PrescriptionSerializer


class PrescriptionListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        prescriptions = Prescription.objects.all()

        serializer = PrescriptionSerializer(
            prescriptions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'doctor':
            return Response(
                {
                    'error': 'Only doctors can create prescriptions'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PrescriptionSerializer(
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


class PrescriptionDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return Prescription.objects.get(pk=pk)

    def get(self, request, pk):

        prescription = self.get_object(pk)

        serializer = PrescriptionSerializer(
            prescription
        )

        return Response(serializer.data)
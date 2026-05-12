from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        patients = Patient.objects.all()

        serializer = PatientSerializer(
            patients,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'admin':
            return Response(
                {
                    'error': 'Only admin can create patients'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PatientSerializer(
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


class PatientDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return Patient.objects.get(pk=pk)

    def get(self, request, pk):

        patient = self.get_object(pk)

        serializer = PatientSerializer(patient)

        return Response(serializer.data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        appointments = Appointment.objects.all()

        serializer = AppointmentSerializer(
            appointments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = AppointmentSerializer(
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


class AppointmentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return Appointment.objects.get(pk=pk)

    def get(self, request, pk):

        appointment = self.get_object(pk)

        serializer = AppointmentSerializer(
            appointment
        )

        return Response(serializer.data)

    def patch(self, request, pk):

        appointment = self.get_object(pk)

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):

        appointment = self.get_object(pk)

        appointment.status = 'cancelled'
        appointment.save()

        return Response({
            'message': 'Appointment cancelled successfully'
        })
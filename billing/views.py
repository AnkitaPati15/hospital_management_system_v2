from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Bill
from .serializers import BillSerializer


class BillListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        bills = Bill.objects.all()

        serializer = BillSerializer(
            bills,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'admin':
            return Response(
                {
                    'error': 'Only admin can generate bills'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BillSerializer(
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


class BillDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        return Bill.objects.get(pk=pk)

    def get(self, request, pk):

        bill = self.get_object(pk)

        serializer = BillSerializer(bill)

        return Response(serializer.data)

    def patch(self, request, pk):

        bill = self.get_object(pk)

        serializer = BillSerializer(
            bill,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)
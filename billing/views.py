from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import (
ListView,
CreateView,
UpdateView,
DeleteView,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.permission import IsAdmin

from .models import Bill
from .serializers import BillSerializer

# ==================================

# FRONTEND VIEWS

# ==================================

class BillListView(ListView):
    model = Bill

    template_name = 'billing/bill_list.html'

    context_object_name = 'bills'

    queryset = Bill.objects.select_related('patient', 'appointment')

class BillCreateView(CreateView):
    model = Bill

    fields = [
        'patient',
        'appointment',
        'amount',
        'payment_status',
        'payment_method',
    ]

    template_name = 'billing/bill_form.html'

    success_url = reverse_lazy('bill-list')

class BillUpdateView(UpdateView):
    model = Bill

    fields = [
        'amount',
        'payment_status',
        'payment_method',
    ]

    template_name = 'billing/bill_form.html'

    success_url = reverse_lazy('bill-list')

class BillDeleteView(DeleteView):
    model = Bill

    template_name = 'billing/bill_confirm_delete.html'

    success_url = reverse_lazy('bill-list')

# ==================================

# API VIEWS

# ==================================

class BillListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

    def post(self, request):
        if getattr(request.user, 'role', None) != 'admin':
            return Response({'error': 'Only admin can generate bills'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BillDetailView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        return get_object_or_404(Bill, pk=pk)

    def get(self, request, pk):
        bill = self.get_object(pk)
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    def patch(self, request, pk):
        bill = self.get_object(pk)
        serializer = BillSerializer(bill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

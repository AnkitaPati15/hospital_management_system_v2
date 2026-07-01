from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Department
from .serializers import DepartmentSerializer
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.permission import (
    IsAdmin
)


class DepartmentCreateView(CreateView):

    model = Department

    fields = [
        'name',
        'description'
    ]

    template_name = (
        'departments/department_form.html'
    )

    success_url = reverse_lazy(
        'department-list'
    )

class DepartmentListView(ListView):

    model = Department

    template_name = (
        'departments/department_list.html'
    )

    context_object_name = (
        'departments'
    )

class DepartmentUpdateView(UpdateView):

    model = Department

    fields = [
        'name',
        'description'
    ]

    template_name = (
        'departments/department_form.html'
    )

    success_url = reverse_lazy(
        'department-list'
    )

class DepartmentDeleteView(DeleteView):

    model = Department

    template_name = (
        'departments/department_confirm_delete.html'
    )

    success_url = reverse_lazy(
        'department-list'
    )

class DepartmentListCreateView(APIView):

    permission_classes = [
        IsAdmin
    ]

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
                    'error':
                    'Only admin can create department'
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
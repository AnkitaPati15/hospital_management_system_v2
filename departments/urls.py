
from django.urls import path

from .views import (
    DepartmentListCreateView,
    DepartmentListView,
    DepartmentUpdateView,
    DepartmentDeleteView,
    DepartmentCreateView
)
urlpatterns = [

    # API

    path(
        '',
        DepartmentListCreateView.as_view(),
        name='department-api'
    ),

    # Frontend

    path(
        'ui/',
        DepartmentListView.as_view(),
        name='department-list'
    ),

    path(
        'ui/<int:pk>/edit/',
        DepartmentUpdateView.as_view(),
        name='department-update'
    ),

    path(
        'ui/<int:pk>/delete/',
        DepartmentDeleteView.as_view(),
        name='department-delete'
    ),
    path(
    'ui/create/',
    DepartmentCreateView.as_view(),
    name='department-create'
),

]
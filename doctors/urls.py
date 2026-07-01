from django.urls import path

from .views import (
    DoctorListCreateView,
    DoctorDetailView,

    DoctorListView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView,
    doctor_dashboard
)

urlpatterns = [

    # API

    path(
        '',
        DoctorListCreateView.as_view(),
        name='doctor-api'
    ),

    path(
        '<int:pk>/',
        DoctorDetailView.as_view(),
        name='doctor-detail'
    ),

    # FRONTEND

    path(
        'ui/',
        DoctorListView.as_view(),
        name='doctor-list'
    ),

    path(
        'ui/create/',
        DoctorCreateView.as_view(),
        name='doctor-create'
    ),

    path(
        'ui/<int:pk>/edit/',
        DoctorUpdateView.as_view(),
        name='doctor-update'
    ),

    path(
        'ui/<int:pk>/delete/',
        DoctorDeleteView.as_view(),
        name='doctor-delete'
    ),
    path(

    'dashboard/',

    doctor_dashboard,

    name='doctor-dashboard'

),

]
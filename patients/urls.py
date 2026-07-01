from django.urls import path

from .views import (
    PatientBillListView,
    PatientDashboardView,
    PatientListCreateView,
    PatientDetailView,
    PatientListView,
    PatientCreateView,
    PatientPrescriptionListView,
    PatientUpdateView,
    PatientDeleteView,
    PatientAppointmentListView
)


urlpatterns = [
    # API URLs
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    # Frontend URLs
    path('ui/', PatientListView.as_view(), name='patient-list'),
    path('ui/create/', PatientCreateView.as_view(), name='patient-create'),
    path('ui/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient-update'),
    path('ui/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
    path(
    'dashboard/',
    PatientDashboardView.as_view(),
    name='patient-dashboard'
),
path(
    'my-appointments/',
    PatientAppointmentListView.as_view(),
    name='my-appointments'
),
path(
    'my-prescriptions/',
    PatientPrescriptionListView.as_view(),
    name='my-prescriptions'
),
path(
    'my-bills/',
    PatientBillListView.as_view(),
    name='my-bills'
),
]

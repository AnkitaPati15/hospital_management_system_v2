from django.urls import path

from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,

    AppointmentListView,
    AppointmentCreateView,  
    AppointmentUpdateView,
    AppointmentDeleteView,
    BookAppointmentView,
)

urlpatterns = [

    # API

    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # Frontend

    path('ui/', AppointmentListView.as_view(), name='appointment-list'),
    path('ui/create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('ui/<int:pk>/edit/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('ui/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment-delete'),
    path(
    'book/',
    BookAppointmentView.as_view(),
    name='appointment-book'
),
]
from django.urls import path

from .views import (
    PrescriptionListCreateView,
    PrescriptionDetailView,

    PrescriptionListView,
    PrescriptionCreateView,
    PrescriptionUpdateView,
    PrescriptionDeleteView,
)


urlpatterns = [
    # API URLs
    path('', PrescriptionListCreateView.as_view(), name='prescription-list-create'),
    path('<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),

    # Frontend URLs
    path('ui/', PrescriptionListView.as_view(), name='prescription-list'),
    path('ui/create/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('ui/<int:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription-update'),
    path('ui/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription-delete'),
]

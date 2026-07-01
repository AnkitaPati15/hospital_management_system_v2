from django.urls import path

from .views import (
    BillListCreateView,
    BillDetailView,

    BillListView,
    BillCreateView,
    BillUpdateView,
    BillDeleteView,
)


urlpatterns = [
    # API URLs
    path('', BillListCreateView.as_view(), name='bill-list-create'),
    path('<int:pk>/', BillDetailView.as_view(), name='bill-detail'),

    # Frontend URLs
    path('ui/', BillListView.as_view(), name='bill-list'),
    path('ui/create/', BillCreateView.as_view(), name='bill-create'),
    path('ui/<int:pk>/edit/', BillUpdateView.as_view(), name='bill-update'),
    path('ui/<int:pk>/delete/', BillDeleteView.as_view(), name='bill-delete'),
]

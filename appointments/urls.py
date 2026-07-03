from django.urls import path

from .views import (
    AppointmentListCreateView,
    AppointmentDetailView,

    AppointmentListView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    BookAppointmentView,

    ApproveAppointmentView,
    RejectAppointmentView,
    CompleteAppointmentView,
)

urlpatterns = [

    # ==========================
    # API
    # ==========================

    path(
        "",
        AppointmentListCreateView.as_view(),
        name="appointment-list-create",
    ),

    path(
        "<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),

    # ==========================
    # Frontend
    # ==========================

    path(
        "ui/",
        AppointmentListView.as_view(),
        name="appointment-list",
    ),

    path(
        "ui/create/",
        AppointmentCreateView.as_view(),
        name="appointment-create",
    ),

    path(
        "ui/<int:pk>/edit/",
        AppointmentUpdateView.as_view(),
        name="appointment-update",
    ),

    path(
        "ui/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment-delete",
    ),

    path(
        "book/",
        BookAppointmentView.as_view(),
        name="appointment-book",
    ),

    # ==========================
    # Doctor Workflow
    # ==========================

    path(
        "ui/<int:pk>/approve/",
        ApproveAppointmentView.as_view(),
        name="appointment-approve",
    ),

    path(
        "ui/<int:pk>/reject/",
        RejectAppointmentView.as_view(),
        name="appointment-reject",
    ),

    path(
        "ui/<int:pk>/complete/",
        CompleteAppointmentView.as_view(),
        name="appointment-complete",
    ),
]
"""
URL configuration for hospital_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Hospital Management API",
        default_version="v1",
        description="API documentation for Hospital Management System",
        contact=openapi.Contact(
            email="admin@citycarehospital.com"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [

    # ==================================
    # HOME PAGE
    # ==================================

    path(
        "",
        RedirectView.as_view(
            pattern_name="login-page",
            permanent=False,
        ),
    ),

    # ==================================
    # SWAGGER
    # ==================================

    path(
        "swagger/",
        schema_view.with_ui(
            "swagger",
            cache_timeout=0,
        ),
        name="schema-swagger-ui",
    ),

    path(
        "redoc/",
        schema_view.with_ui(
            "redoc",
            cache_timeout=0,
        ),
        name="schema-redoc",
    ),

    # ==================================
    # DJANGO ADMIN
    # ==================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ==================================
    # ACCOUNTS
    # ==================================

    path(
        "api/auth/",
        include("accounts.urls"),
    ),

    # ==================================
    # DEPARTMENTS
    # ==================================

    path(
        "api/departments/",
        include("departments.urls"),
    ),

    # ==================================
    # DOCTORS
    # ==================================

    path(
        "api/doctors/",
        include("doctors.urls"),
    ),

    # ==================================
    # PATIENTS
    # ==================================

    path(
        "api/patients/",
        include("patients.urls"),
    ),

    # ==================================
    # APPOINTMENTS
    # ==================================

    path(
        "api/appointments/",
        include("appointments.urls"),
    ),

    # ==================================
    # PRESCRIPTIONS
    # ==================================

    path(
        "api/prescriptions/",
        include("prescriptions.urls"),
    ),

    # ==================================
    # BILLING
    # ==================================

    path(
        "api/bills/",
        include("billing.urls"),
    ),

    # ==================================
    # DASHBOARD
    # ==================================

    path(
        "dashboard/",
        include("dashboard.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
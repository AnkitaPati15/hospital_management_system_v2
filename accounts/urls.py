from django.urls import path

from .views import (
    RegisterPageView,
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    login_page,
    logout_page,
    register_choice,
    doctor_register,
    patient_register,
)

urlpatterns = [
    # =========================
    # API URLs
    # =========================
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # =========================
    # Frontend URLs
    # =========================
    path('register-ui/', RegisterPageView.as_view(), name='register-page'),
    path('login-ui/', login_page, name='login-page'),
    path('logout-ui/', logout_page, name='logout-page'),
    path(
    'register-choice/',
    register_choice,
    name='register-choice'
),

path(
    'doctor-register/',
    doctor_register,
    name='doctor-register'
),

path(
    'patient-register/',
    patient_register,
    name='patient-register'
),
]

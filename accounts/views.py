from django.shortcuts import render, redirect

from django.contrib.auth import (
authenticate,
login,
logout
)

from django.views.generic import CreateView
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User
from .forms import RegisterForm
from .serializers import RegisterSerializer
from doctors.models import Doctor
from patients.models import Patient
from departments.models import Department

from .forms import (
    DoctorRegisterForm,
    PatientRegisterForm
)


def register_choice(request):

    return render(
        request,
        'accounts/register_choice.html'
    )

def doctor_register(request):

    if request.method == 'POST':

        form = DoctorRegisterForm(
            request.POST
        )

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data['username'],

                email=form.cleaned_data['email'],

                password=form.cleaned_data['password'],

                role='doctor'
            )

            Doctor.objects.create(

                user=user,

                department=form.cleaned_data['department'],

                qualification=form.cleaned_data['qualification'],

                experience=form.cleaned_data['experience'],

                consultation_fee=form.cleaned_data['consultation_fee']
            )

            return redirect(
                'login-page'
            )

    else:

        form = DoctorRegisterForm()

    return render(
        request,
        'accounts/doctor_register.html',
        {
            'form': form
        }
    )


def patient_register(request):

    if request.method == 'POST':

        form = PatientRegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data['username'],

                email=form.cleaned_data['email'],

                password=form.cleaned_data['password'],

                role='patient'
            )

            Patient.objects.create(

                user=user,

                age=form.cleaned_data['age'],

                gender=form.cleaned_data['gender'],

                blood_group=form.cleaned_data['blood_group'],

                phone_number=form.cleaned_data['phone_number'],

                address=form.cleaned_data['address'],

                emergency_contact=form.cleaned_data['emergency_contact'],

                medical_history=form.cleaned_data['medical_history']
            )

            return redirect('login-page')

    else:

        form = PatientRegisterForm()

    return render(
        request,
        'accounts/patient_register.html',
        {
            'form': form
        }
    )
     

# ==================================

# FRONTEND VIEWS

# ==================================

class RegisterPageView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login-page')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login-page')

def login_page(request):

    if request.method == "POST":

        email = request.POST.get("email")

        password = request.POST.get("password")

        user = authenticate(

            request,

            email=email,

            password=password

        )

        if user is not None:

            login(request, user)

            if user.role == "admin":

              return redirect("admin-dashboard")

            elif user.role == "doctor":

             return redirect("doctor-dashboard")

            elif user.role == "patient":

             return redirect("patient-dashboard")
        return render(

            request,

            "accounts/login.html",

            {

                "error": "Invalid Email or Password"

            }

        )

    return render(

        request,

        "accounts/login.html"

    )


def logout_page(request):
    logout(request)
    return redirect('login-page')

# ==================================

# API VIEWS

# ==================================

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,username=email,password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({
            'email': request.user.email,
            'username': request.user.username,
            'role': request.user.role,
        })

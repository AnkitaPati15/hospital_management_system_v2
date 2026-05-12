from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import RegisterSerializer


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'message': 'User registered successfully'
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            return Response({
                'message': 'Login successful'
            })

        return Response(
            {
                'error': 'Invalid credentials'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        logout(request)

        return Response({
            'message': 'Logout successful'
        })


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            'email': request.user.email,
            'role': request.user.role
        })
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes, action

from .models import Company, Employee, Device, DeviceLog, CheckOut
from .serializers import CompanySerializer, EmployeeSerializer, DeviceSerializer, DeviceLogSerializer, CheckOutSerializer

# Create your views here.
#signup
@api_view(['GET','POST'])
@permission_classes([AllowAny])
def signupView(request):
    username = request.data.get('username')
    password = request.data.get('password')
    c_name = request.data.get('c_name')
    c_email = request.data.get('c_email')

    if not username or not password or not c_name or not c_email:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    Company.objects.create(name=c_name, email=c_email, owner=user)
    return JsonResponse({'status': 'Successfully registered.'})

#login
@api_view(['POST'])
@permission_classes([AllowAny])
def loginView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username = username, password = password)
    if user:
        login(request, user)
        return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#logout
@api_view(['POST'])
def logoutView(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

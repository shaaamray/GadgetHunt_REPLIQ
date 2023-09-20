from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes, action

from .models import Company, Employee, Device, DeviceLog, CheckOut
from .serializers import (
    CompanySerializer,
    EmployeeSerializer,
    DeviceSerializer,
    DeviceLogSerializer,
    CheckOutSerializer,
    AssignDeviceSerializer,
    ReceiveDeviceSerializer
)


# Create your views here.
# signup
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def signupView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    c_name = request.data.get("c_name")
    c_email = request.data.get("c_email")

    if not username or not password or not c_name or not c_email:
        return Response(
            {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    Company.objects.create(name=c_name, email=c_email, owner=user)
    return Response({"SignUP is Successful"}, status=status.HTTP_201_CREATED)


# login
@api_view(["POST"])
@permission_classes([AllowAny])
def loginView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(
            {"error": "Both username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response(
            {"message": "Logged in successfully"}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


# logout
@api_view(["POST"])
def logoutView(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return Response(
                {"detail": "You don't own a company."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "name": request.data.get("name"),
            "position": request.data.get("position"),
            "devices": request.data.get("devices", []),
            "company": company.id,  # logged-in user ID
        }

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return Response(
                {"detail": "No access to company"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "d_name": request.data.get("d_name"),
            "type": request.data.get("type"),
            "description": request.data.get("description"),
        }

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            device = serializer.save()
            company.devices.add(device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "assign_device":
            return AssignDeviceSerializer
        elif self.action == "rec_device":
            return ReceiveDeviceSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def assign_device(self, request, pk=None):
        print(request.user)
        try:
            owner = Company.objects.get(owner=request.user)
            print(owner)
        except Company.DoesNotExist:
            return Response(
                {"detail": "No access to company"}, status=status.HTTP_400_BAD_REQUEST
            )

        employee_id = request.data.get("employee_id")
        condition_on_checkout = request.data.get("condition_on_checkout")

        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Invalid employee ID provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        device_id = self.kwargs.get("pk")

        try:
            device = owner.devices.get(id=device_id)
        except Device.DoesNotExist:
            return Response(
                {"error": "Invalid device ID provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if device.current_holder:
            return Response(
                {"error": "Device is already assigned to another employee."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        previous_device_log = device.dev_logInfo.first()
        previous_checkout = device.checkout_records.first()
        if previous_device_log:
            previous_device_log.delete()
        if previous_checkout:
            previous_checkout.delete()

        device.current_holder = employee
        device.save()

        employee.devices.add(device)

        checkout = CheckOut(
            employee=employee, device=device, check_out_date=datetime.now, return_date = ""
        )
        checkout.save()
        device_log = DeviceLog(
            company = owner,
            device=device,
            check_out=checkout,
            condition_on_check_out=condition_on_checkout,
            condition_on_return="",
        )
        device_log.save()

        return Response(
            {"message": "Device assigned successfully."}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def rec_device(self, request, pk=None):
        try:
            owner = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            return Response(
                {"detail": "No access to company"}, status=status.HTTP_400_BAD_REQUEST
            )

        device_id = self.kwargs.get("pk")
        try:
            device = owner.devices.get(id=device_id)
        except Device.DoesNotExist:
            return Response(
                {"error": "Invalid device ID provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not device.current_holder:
            return Response(
                {"error": "Device is not currently assigned to an employee."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee_id = request.data.get("employee_id")
        employee = Employee.objects.get(id= employee_id)
        employee.devices.remove(device)
        condition_on_return = request.data.get("condition_on_return")

        device_log = DeviceLog(
            company=owner,
            device=device,
            check_out=device.checkout_records.get(device=device),
            # condition_on_check_out=device.checkout_records.get(device=device).condition_on_check_out,
            condition_on_return=condition_on_return,
        )
        device_log.save()

        checkout = device.checkout_records.get(device=device)
        checkout.return_date = datetime.now()
        checkout.save()

        device.current_holder = None
        device.save()

        return Response(
            {"message": "Device has been taken back successfully."},
            status=status.HTTP_200_OK,
        )
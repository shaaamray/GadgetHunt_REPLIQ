from rest_framework import serializers
from .models import Company, Employee, Device, DeviceLog, CheckOut

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'owner', 'name', 'email', 'devices', 'employees', 'device_logs', 'checkouts']

class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'company', 'devices']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'd_name', 'type', 'description']

class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = ['id', 'device', 'check_out', 'date', 'condition_on_check_out', 'condition_on_return']

class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = ['id', 'employee', 'device', 'check_out_date', 'return_date']

CompanySerializer.employees = EmployeeSerializer(many=True, read_only=True)
CompanySerializer.device_logs = DeviceLogSerializer(many=True, read_only=True, source='device_logs')
CompanySerializer.checkouts = CheckOutSerializer(many=True, source='checkout_records')
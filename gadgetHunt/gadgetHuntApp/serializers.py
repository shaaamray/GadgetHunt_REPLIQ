from rest_framework import serializers
from .models import Company, Employee, Device, DeviceLog, CheckOut

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'owner', 'name', 'email', 'devices', 'employees', 'device_logs', 'checkouts']

class EmployeeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(EmployeeSerializer, self).__init__(*args, **kwargs)
        
        request = self.context.get('request')
        if request:
            owned_company = Company.objects.filter(owner=request.user)
            self.fields['company'].queryset = owned_company

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    devices = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all(), many=True, required=False, allow_empty = True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'position', 'company', 'devices']
        extra_kwargs = {'devices': {'required': False}}

    def create(self, validated_data):
        devices = validated_data.pop('devices', [])
        employee = Employee.objects.create(**validated_data)
        for device in devices:
            employee.devices.add(device)
        return employee

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'd_name', 'type', 'description']

class DeviceLogSerializer(serializers.ModelSerializer):
    check_out_date = serializers.DateTimeField(source='check_out.check_out_date', read_only=True)
    return_date = serializers.DateTimeField(source='check_out.return_date', read_only=True)

    class Meta:
        model = DeviceLog
        fields = ['id', 'device', 'check_out_date', 'return_date', 'condition_on_check_out', 'condition_on_return']

class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = ['id', 'employee', 'device', 'check_out_date', 'return_date']

CompanySerializer.employees = EmployeeSerializer(many=True, read_only=True)
CompanySerializer.device_logs = DeviceLogSerializer(many=True, read_only=True, source='device_logs')
CompanySerializer.checkouts = CheckOutSerializer(many=True, source='checkout_records')
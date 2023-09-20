from django.contrib import admin
from .models import Company, Employee, Device, DeviceLog, CheckOut

# Register your models here.
#superuser -- username: admin -- password: 12345678

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'email', 'list_employees', 'list_devices')

    def list_employees(self, obj):
        return ", ".join([employee.name for employee in obj.employees.all()])
    list_employees.short_description = 'Employees'
    
    def list_devices(self, obj):
        return ", ".join([device.d_name for device in obj.devices.all()])
    list_devices.short_description = 'Devices'

admin.site.register(Company, CompanyAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'company', 'list_assigned_devices')

    def list_assigned_devices(self, obj):
        assigned_devices = obj.devices.all()
        print(assigned_devices)
        return ", ".join([device.d_name for device in obj.devices.all()])
    list_assigned_devices.short_description = 'Assigned Devices'

admin.site.register(Employee, EmployeeAdmin)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'd_name', 'type', 'description')

admin.site.register(Device, DeviceAdmin)

class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'check_out', 'date', 'condition_on_check_out', 'condition_on_return')

admin.site.register(DeviceLog, DeviceLogAdmin)

class CheckOutAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'device', 'check_out_date', 'return_date')

admin.site.register(CheckOut, CheckOutAdmin)
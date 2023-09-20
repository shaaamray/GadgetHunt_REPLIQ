from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError

# Create your models here.

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies', null = True)
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    devices = models.ManyToManyField('Device', related_name='companies')

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    POSITION_CHOICES = [
        ('Software Eng', 'Software Eng'),
        ('Network Eng', 'Network Eng'),
        ('Line Manager', 'Line Manager'),
        ('QA Eng', 'QA Eng'),
        ('Testing Engineer', 'Testing Engineer'),
    ]
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    devices = models.ManyToManyField('Device', related_name='holders')

    def clean(self):
        
        for device in self.devices.all():
            if device.company != self.company:
                raise ValidationError(f"This {device.d_name} don't belong to {self.company.name} company")

    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        self.clean() 

    def __str__(self):
        return self.name
    
class Device(models.Model):
    d_name = models.CharField(max_length=100)
    DEVICE_TYPE_CHOICES = [
        ('phone', 'phone'),
        ('tablet', 'tablet'),
        ('laptop', 'laptop'),
        ('headphone', 'headphone'),
    ]
    type = models.CharField(max_length=100, choices=DEVICE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    current_holder = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_devices")

    def __str__(self):
        return self.d_name
    
class CheckOut(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='checkout_records')
    check_out_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.company:
            self.company = self.employee.company
        super(CheckOut, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} checked out {self.device}"
    
class DeviceLog(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="device_logs")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="dev_logInfo")
    check_out = models.ForeignKey(CheckOut, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    CONDITION_CHOICES = [
        ('Excellent','Excellent'),
        ('Good','Good'),
        ('Average','Average'),
        ('Below avg','Below avg'),
        ('Poor','Poor')
    ]
    condition_on_check_out = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    condition_on_return = models.CharField(max_length=20, choices=CONDITION_CHOICES)

    def save(self, *args, **kwargs):
        if not self.company:
            self.company = self.check_out.company
        super(DeviceLog, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.device} - {self.date.strftime('%Y-%m-%d')}"


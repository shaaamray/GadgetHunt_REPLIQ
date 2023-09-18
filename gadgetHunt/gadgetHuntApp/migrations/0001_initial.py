# Generated by Django 4.2.5 on 2023-09-18 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CheckOut",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_out_date", models.DateTimeField(auto_now_add=True)),
                ("return_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("d_name", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("phone", "phone"),
                            ("tablet", "tablet"),
                            ("laptop", "laptop"),
                            ("headphone", "headphone"),
                        ],
                        max_length=100,
                    ),
                ),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("Software Eng", "Software Eng"),
                            ("Network Eng", "Network Eng"),
                            ("Line Manager", "Line Manager"),
                            ("QA Eng", "QA Eng"),
                            ("Testing Engineer", "Testing Engineer"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employees",
                        to="gadgetHuntApp.company",
                    ),
                ),
                (
                    "devices",
                    models.ManyToManyField(
                        related_name="holders", to="gadgetHuntApp.device"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeviceLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "condition_on_check_out",
                    models.CharField(
                        choices=[
                            ("Excellent", "Excellent"),
                            ("Good", "Good"),
                            ("Average", "Average"),
                            ("Below avg", "Below avg"),
                            ("Poor", "Poor"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "condition_on_return",
                    models.CharField(
                        choices=[
                            ("Excellent", "Excellent"),
                            ("Good", "Good"),
                            ("Average", "Average"),
                            ("Below avg", "Below avg"),
                            ("Poor", "Poor"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "check_out",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gadgetHuntApp.checkout",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_logs",
                        to="gadgetHuntApp.company",
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gadgetHuntApp.device",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="company",
            name="devices",
            field=models.ManyToManyField(
                related_name="companies", to="gadgetHuntApp.device"
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_companies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="checkout",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="gadgetHuntApp.company",
            ),
        ),
        migrations.AddField(
            model_name="checkout",
            name="device",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="checkout_records",
                to="gadgetHuntApp.device",
            ),
        ),
        migrations.AddField(
            model_name="checkout",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="gadgetHuntApp.employee"
            ),
        ),
    ]

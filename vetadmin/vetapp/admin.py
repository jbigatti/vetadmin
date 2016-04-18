"""Register your models here in alphabetic order."""
from django.contrib import admin

from .models import CarouselSlide, MedicalRecord, Patient, VaccinationRecord


@admin.register(CarouselSlide)
class CarouselAdmin(admin.ModelAdmin):

    actions = None

    def delete_model(self, request, obj):
        obj.image.delete()
        super().delete_model(request, obj)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    pass
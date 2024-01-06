from django.contrib import admin
from .model import (
    Institution, Faculty, Program, Major, Course,
    City, Governorate, InstituteCategory, AccountType,
    InstitutionType, AccreditationStatus, 
)

# Register your models here.
admin.site.register(Institution)
admin.site.register(Faculty)
admin.site.register(Program)
admin.site.register(Major)
admin.site.register(Course)
admin.site.register(City)
admin.site.register(Governorate)
admin.site.register(InstituteCategory)
admin.site.register(AccountType)
admin.site.register(InstitutionType)
admin.site.register(AccreditationStatus)

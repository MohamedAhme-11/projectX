# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter  
from .views import LegislatorViewSet, FacultyCriteriaViewSet, MajorCriteriaViewSet, CourseCriteriaViewSet  # Update the import according to your app's structure

# Creating a router and registering our viewsets with it.
router = DefaultRouter()
router.register(r'legislators', LegislatorViewSet)
router.register(r'faculty-criteria', FacultyCriteriaViewSet)
router.register(r'major-criteria', MajorCriteriaViewSet)
router.register(r'course-criteria', CourseCriteriaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    
]

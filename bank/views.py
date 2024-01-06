# views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .model import Legislator, FacultyCriteria, MajorCriteria, CourseCriteria
from .serializers import (
    LegislatorSerializer,
    FacultyCriteriaSerializer,
    MajorCriteriaSerializer,
    CourseCriteriaSerializer,
)
from .permissions import IsLegislator

class LegislatorViewSet(viewsets.ViewSet):
    """
    A viewset that provides actions for Legislator to register, login,
    and manage criteria for faculty, major, and course.
    """

    permission_classes_by_action = {
        'create': [permissions.AllowAny],
        'add_faculty_criteria': [IsLegislator],
        'add_major_criteria': [IsLegislator],
        'add_course_criteria': [IsLegislator],
        # Add other actions if necessary
    }

    def create(self, request):
        """
        Register a new legislator and return a token for authentication.
        """
        serializer = LegislatorSerializer(data=request.data)
        if serializer.is_valid():
            legislator = serializer.save()
            token, created = Token.objects.get_or_create(user=legislator.user)
            return Response({
                "message": "Legislator successfully registered",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='add-faculty-criteria')
    def add_faculty_criteria(self, request):
        """
        Add new faculty criteria linked to the legislator.
        """
        serializer = FacultyCriteriaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(legislator=request.user.legislator)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='add-major-criteria')
    def add_major_criteria(self, request):
        """
        Add new major criteria linked to the legislator.
        """
        serializer = MajorCriteriaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(legislator=request.user.legislator)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='add-course-criteria')
    def add_course_criteria(self, request):
        """
        Add new course criteria linked to the legislator.
        """
        serializer = CourseCriteriaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(legislator=request.user.legislator)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


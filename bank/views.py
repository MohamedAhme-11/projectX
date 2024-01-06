# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .model import FacultyCriteria, Course, Faculty, FacultyCriteria
from .serializers import FacultyCriteriaSerializer, CourseSerializer, LegislatorSerializer,FacultyCriteriaSerializer
from .permissions import IsLegislator
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LegislatorCreateAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LegislatorSerializer(data=request.data)
        if serializer.is_valid():
            legislator = serializer.save()
            user = authenticate(username=legislator.user.username, password=request.data['password'])
            token, created = Token.objects.get_or_create(user=legislator.user)
            return Response({"message": "Legislator successfully registered", "token": token.key}, status=201)
        return Response(serializer.errors, status=400)


    
class FacultyCriteriaCreateView(generics.CreateAPIView):
    queryset = FacultyCriteria.objects.all()
    serializer_class = FacultyCriteriaSerializer
    permission_classes = [IsLegislator]

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # Extract faculty name from the request data
        faculty_name = serializer.validated_data.get('faculty_name', None)

        if faculty_name:
            # Attempt to retrieve the corresponding Faculty object
            faculty = Faculty.objects.filter(name_en=faculty_name).first()
            if not faculty:
                # If faculty with the provided name does not exist, raise an error
                raise ValidationError({"faculty_name": "Faculty name is invalid or does not exist."})
            serializer.save(faculty=faculty)
        else:
            # If faculty_name is not provided, raise an error
            raise ValidationError({"faculty_name": "Faculty name is required."})

    def create(self, request, *args, **kwargs):
        # Handle bulk course creation
        if isinstance(request.data, list):
            courses_data = request.data
            responses = []
            for course_data in courses_data:
                serializer = self.get_serializer(data=course_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                responses.append(serializer.data)
            return Response(responses, status=status.HTTP_201_CREATED)
        else:
            # Handle single course creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsLegislator]



class AddFacultyCriteriaAPIView(generics.CreateAPIView):
    serializer_class = FacultyCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(legislator=self.request.user)

# Similar views for Major Criteria and Course Criteria

class DeleteFacultyCriteriaAPIView(generics.DestroyAPIView):
    queryset = FacultyCriteria.objects.all()
    serializer_class = FacultyCriteriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        legislator = self.request.user
        return FacultyCriteria.objects.filter(legislator=legislator)

# Similar views for updating and deleting Major Criteria and Course Criteria


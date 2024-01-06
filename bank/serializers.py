# serializers.py
from rest_framework import serializers
from .model import CustomUser, Legislator, FacultyCriteria, MajorCriteria, CourseCriteria, Course
from django.contrib.auth.hashers import make_password

class LegislatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    # New fields
    location_branch_name_en = serializers.CharField()
    location_branch_name_ar = serializers.CharField()
    primary_contact_name = serializers.CharField()
    website = serializers.URLField()
    country = serializers.CharField()
    governorate = serializers.CharField()
    city = serializers.CharField()
    phone = serializers.CharField()
    landline = serializers.CharField()
    show_on_qodourat = serializers.BooleanField()

    class Meta:
        model = Legislator
        fields = ['name_en', 'name_ar', 'email', 'password', 'password2',
                  'location_branch_name_en', 'location_branch_name_ar', 
                  'primary_contact_name', 'website', 'country', 'governorate', 
                  'city', 'phone', 'landline', 'show_on_qodourat']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        # Creating user data and removing legislator-specific data
        user_data = {
            'username': validated_data.get('email'),  # Assuming email is used as username
            'email': validated_data.pop('email'),
            # ... include other user-specific fields if necessary ...
        }
        password = validated_data.pop('password')
        validated_data.pop('password2', None)

        # Create CustomUser instance
        user = CustomUser.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Create Legislator instance linked to the user
        # Ensure only legislator-specific fields are left in validated_data
        legislator = Legislator.objects.create(user=user, **validated_data)

        return legislator

class FacultyCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyCriteria
        fields = '__all__'  # Include the fields you want to expose

class MajorCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCriteria
        fields = '__all__'  # Include the fields you want to expose

class CourseCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCriteria
        fields = '__all__'  # Include the fields you want to expose

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    
    def create(self, validated_data):
        # Handle list of course data
        courses = [Course(**item) for item in validated_data]
        return Course.objects.bulk_create(courses)


class FacultyCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyCriteria
        fields = '__all__'  # Include the fields you want to expose

class MajorCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCriteria
        fields = '__all__'  # Include the fields you want to expose

class CourseCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCriteria
        fields = '__all__'  # Include the fields you want to expose

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    
    def create(self, validated_data):
        # Handle list of course data
        courses = [Course(**item) for item in validated_data]
        return Course.objects.bulk_create(courses)
    

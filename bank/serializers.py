from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from cities.models import City
from .model import CustomUser, Legislator, FacultyCriteria, MajorCriteria, CourseCriteria
from rest_framework.exceptions import ValidationError

class LegislatorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField( write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Confirm password field
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False)
    country = serializers.CharField(default="Default Country")

    class Meta:
        model = Legislator
        fields = ('name_en', 'name_ar', 'email', 'city', 'password', 'password2', 
                  'location_branch_name_en', 'location_branch_name_ar', 'primary_contact_name',
                  'website', 'country', 'show_on_qodourat')  # Add 'password2' to fields

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2', None):
            raise ValidationError({"password2": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user_data = {
            'username': validated_data.get('email'),
            'email': validated_data.get('email'),
            'first_name': validated_data.get('name_en', ''),
            'last_name': validated_data.get('name_ar', ''),
            # ... potentially other fields ...
        }
        user = CustomUser.objects.create(**user_data)
        user.set_password(validated_data['password'])
        user.save()

        # Extract city and use it to set the country
        city = validated_data.get('city')
        if city:
            # Make sure your City model has a 'country' field that points to a Country model
            validated_data['country'] = city.country.name

        # Remove password and password2 fields as they are write-only and should not be passed to create()
        validated_data.pop('password', None)
        validated_data.pop('password2', None)

        # Create the Legislator object with the modified validated_data
        legislator_data = validated_data
        legislator_data['user'] = user
        legislator = Legislator.objects.create(**legislator_data)
        return legislator

    # ... [rest of the code like validate method] ...
class FacultyCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyCriteria
        fields = '__all__'

class MajorCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCriteria
        fields = '__all__'

class CourseCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCriteria
        fields = '__all__'

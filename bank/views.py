from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .model import Legislator,FacultyCriteria, MajorCriteria, CourseCriteria
from .serializers import LegislatorRegistrationSerializer,FacultyCriteriaSerializer, MajorCriteriaSerializer, CourseCriteriaSerializer
# views.py
from .permissions import IsLegislator


class LegislatorViewSet(viewsets.ModelViewSet):
    queryset = Legislator.objects.all()
    serializer_class = LegislatorRegistrationSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'slug' 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        legislator = serializer.save()
        token, created = Token.objects.get_or_create(user=legislator.user)
        return Response({
            "legislator": LegislatorRegistrationSerializer(legislator, context=self.get_serializer_context()).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=True, methods=['PUT'], permission_classes=[permissions.IsAuthenticated])
    def update_account(self, request, pk=None):
        legislator = self.get_object()
        serializer = self.get_serializer(legislator, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        legislator = self.get_object()
        user = legislator.user
        self.perform_destroy(legislator)
        user.delete()  # Delete the associated user as well
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FacultyCriteriaViewSet(viewsets.ModelViewSet):
    queryset = FacultyCriteria.objects.all()
    serializer_class = FacultyCriteriaSerializer
    permission_classes = [IsLegislator]
    # Add permission classes as needed

class MajorCriteriaViewSet(viewsets.ModelViewSet):
    queryset = MajorCriteria.objects.all()
    serializer_class = MajorCriteriaSerializer
    permission_classes = [IsLegislator]
    # Add permission classes as needed

class CourseCriteriaViewSet(viewsets.ModelViewSet):
    queryset = CourseCriteria.objects.all()
    serializer_class = CourseCriteriaSerializer
    permission_classes = [IsLegislator]
    # Add permission classes as needed

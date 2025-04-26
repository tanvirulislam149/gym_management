from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from plans.models import Plans, Fitness_classes
from plans.serializers import PlansSerializer, FitnessClassSerializer, CreatePlansSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class PlansViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = Plans.objects.all()
    
    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return []

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreatePlansSerializer
        return PlansSerializer


class FitnessClassesViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch","put", "delete", "head", "options"]
    queryset = Fitness_classes.objects.all()
    serializer_class = FitnessClassSerializer
    
    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return []

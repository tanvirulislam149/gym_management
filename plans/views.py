from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from plans.models import Plans, Fitness_classes_category, Scheduled_classes, Review
from plans.serializers import PlansSerializer, FitnessClassSerializer, CreatePlansSerializer, ScheduledClassSerializer, CreateScheduledClassSerializer, ReviewSerializer
from rest_framework.permissions import IsAdminUser
from plans.permissions import IsReviewAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class PlansViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "put", "delete", "head", "options"]
    queryset = Plans.objects.all()
    
    def get_permissions(self):
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return []

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return CreatePlansSerializer
        return PlansSerializer


class FitnessClassesViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch","put", "delete", "head", "options"]
    queryset = Fitness_classes_category.objects.all()
    serializer_class = FitnessClassSerializer
    
    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return []


class ScheduledClassViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("fitness_class_id",)
    http_method_names = ["get", "post", "patch","put", "delete", "head", "options"]
    queryset = Scheduled_classes.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return CreateScheduledClassSerializer
        return ScheduledClassSerializer
    
    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]
        return []


class ReviewViewset(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    # lookup_field = 'pk'

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Review.objects.filter(fitness_class_id = self.kwargs.get("fitness_class_pk"))

    def get_serializer_context(self):
        return {"fitness_class_id": self.kwargs.get("fitness_class_pk")}
    
class AllReviewViewSet(ModelViewSet):
    http_method_names = ["get", "head", "options"]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all().order_by("-rating")[:5]
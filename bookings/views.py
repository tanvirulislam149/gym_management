from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from bookings.models import Book_plans, Book_Fitness_Classes, Payment_plans
from bookings.serializers import BookPlansSerializer, CreateBookPlanSerializer, BookClassSerializer, CreateBookClassSerializer, ClassAttendence, PaymentPlansSerializer, CreatePaymentPlansSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class BookPlansViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_plans.objects.all()
        return Book_plans.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {"user": self.request.user}
        
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return CreateBookPlanSerializer
        return BookPlansSerializer
    

class BookClassesViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method in ["POST", 'PUT']:
            return CreateBookClassSerializer
        return BookClassSerializer
    
    def get_serializer_context(self):
        return {"user": self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_Fitness_Classes.objects.all()
        return Book_Fitness_Classes.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        

class AttendenceViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("scheduled_class_id",)
    http_method_names = ["get", "put"]
    serializer_class = ClassAttendence

    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_Fitness_Classes.objects.all()
        return Book_Fitness_Classes.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

class PaymentPlansViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment_plans.objects.all().order_by("end_date")
        return Payment_plans.objects.filter(booked_plans__user = self.request.user).order_by("end_date")

    def get_serializer_class(self):
        if self.request.method in ['POST', "PUT"]:
            return CreatePaymentPlansSerializer
        return PaymentPlansSerializer
    
    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]


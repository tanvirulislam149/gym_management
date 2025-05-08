from rest_framework import serializers
from plans.models import Plans, Fitness_classes_category, Scheduled_classes
from django.utils.timezone import now

class SimpleFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitness_classes_category
        fields = ["id", "name"]

class PlansSerializer(serializers.ModelSerializer):
    fitness_classes = SimpleFitnessClassSerializer(many=True)
    class Meta:
        model = Plans
        fields = ["id", "type","months", "price", "fitness_classes"]

class CreatePlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "type", "months", "price", "fitness_classes"]


class FitnessClassSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Fitness_classes_category
        fields = ["id", "name", "image", "description"]


class ScheduledClassSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer()
    class Meta:
        model = Scheduled_classes
        fields = ["id", "fitness_class", "date_time", "instructor", "total_seats", "booked_seats", "present_students"]


class CreateScheduledClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduled_classes
        fields = ["fitness_class", "date_time", "instructor", "total_seats"]

    def validate_date_time(self, dateTime):
        if dateTime <= now():
            raise serializers.ValidationError("Date and time must be in the future.")
        return dateTime
from rest_framework import serializers
from plans.models import Plans, Fitness_classes
from django.utils.timezone import now

class SimpleFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitness_classes
        fields = ["id", "name"]

class PlansSerializer(serializers.ModelSerializer):
    fitness_classes = SimpleFitnessClassSerializer(many=True)
    class Meta:
        model = Plans
        fields = ["id", "type", "price", "fitness_classes"]

class CreatePlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "type", "price", "fitness_classes"]


class FitnessClassSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Fitness_classes
        fields = ["id", "name", "image", "description"]

    # def validate_date_time(self, dateTime):
    #     if dateTime <= now():
    #         raise serializers.ValidationError("Date and time must be in the future.")
    #     return dateTime
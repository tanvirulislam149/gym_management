from rest_framework import serializers
from bookings.models import Book_plans, Book_Fitness_Classes, Payment_plans
from plans.models import Plans, Fitness_classes
from decimal import Decimal 
from user.models import CustomUser
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]

class SimplePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "type"]

class BookPlansSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    plans = SimplePlanSerializer()
    current_plan_days = serializers.SerializerMethodField(method_name="get_plan_dates")
    class Meta:
        model = Book_plans
        fields = ["id", "user", "plans", "price", "current_plan_days"]
        read_only_fields = ["user", "price", "current_plan_days"]

    def get_plan_dates(self, book_plans: Book_plans):
        plan = Payment_plans.objects.filter(
            booked_plans_id = book_plans.id,
            start_date__lte=now(),
            end_date__gte=now()
        )[0]
        print(plan, "---------------")
        if plan:
            return f"{plan.start_date} - {plan.end_date}"
        else:
            return "No active plan"

class CreateBookPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_plans
        fields = ["id", "plans"]

    def create(self, validated_data):
        plan = validated_data["plans"]
        user = self.context["user"]
        if Book_plans.objects.filter(user = user).exists():
            raise serializers.ValidationError("You already have booked a plan. Try updating it...")
        
        return Book_plans.objects.create(user = user, price = Decimal(plan.price), **validated_data)

    def update(self, instance, validated_data):
        plan = validated_data["plans"]
        if instance.price > plan.price:  
            raise serializers.ValidationError("You can't update from higher plans to lower plans.")
        
        instance.plans = plan
        instance.price = plan.price
        return super().update(instance, validated_data)


class SimpleFitnessClassSerializerForBooking(serializers.ModelSerializer):
    class Meta:
        model = Fitness_classes
        fields = ["id", "name", "description", "date_time", "instructor"]


class BookClassSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    fitness_class = SimpleFitnessClassSerializerForBooking()
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "user", "fitness_class"]
        read_only_fields = ["user"]

class CreateBookClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Fitness_Classes
        fields = ["fitness_class"]

    def validate_fitness_class(self, fitness_class):
        date_time = fitness_class.date_time
        user = self.context["user"]
        plans = Payment_plans.objects.filter(
            booked_plans__user = user,
            start_date__lte=date_time,
            end_date__gte=date_time
        )
        print(plans, "---------------", date_time)
        if not plans.exists():
            raise serializers.ValidationError("This class is not in between your paid plans.")
        if fitness_class.date_time <= now():
            raise serializers.ValidationError("The date and time must be in the future.")
        return fitness_class

    def create(self, validated_data):
        fitness_class = validated_data["fitness_class"]
        user = self.context["user"]
        if Book_Fitness_Classes.objects.filter(user = user, fitness_class = fitness_class).exists():
            raise serializers.ValidationError("You already have booked for this class.")
        
        return Book_Fitness_Classes.objects.create(user = user, **validated_data)
    
    def update(self, instance, validated_data):
        fitness_class = validated_data["fitness_class"]
        user = self.context["user"]
        if Book_Fitness_Classes.objects.filter(user = user, fitness_class = fitness_class).exists():
            raise serializers.ValidationError("You already have booked for this class.")
        
        return super().update(instance, validated_data)
    

class SimpleBookClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "name", "date_time"]


class ClassAttendence(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    fitness_class = SimpleFitnessClassSerializerForBooking(read_only=True)
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "user", "fitness_class", "attendence"]


class PaymentPlansSerializer(serializers.ModelSerializer):
    booked_plans = BookPlansSerializer()
    class Meta:
        model = Payment_plans
        fields = ["id", "booked_plans", "amount", "start_date", "end_date", "status"]
        read_only_fields = ["amount"]


class CreatePaymentPlansSerializer(serializers.ModelSerializer):
    booked_plans = serializers.UUIDField()
    class Meta:
        model = Payment_plans
        fields = ["id", "booked_plans", "amount", "start_date", "status"]
        read_only_fields = ["amount"]

    def create(self, validated_data):
        planId = validated_data["booked_plans"]
        plan = Book_plans.objects.get(pk = planId)
        if plan.plans.id == 1:
            validated_data["end_date"] = validated_data["start_date"] + relativedelta(months=1)
        elif plan.plans.id == 2:
            validated_data["end_date"] = validated_data["start_date"] + relativedelta(months=3)
        elif plan.plans.id == 3:
            validated_data["end_date"] = validated_data["start_date"] + relativedelta(months=6)
        else:
            validated_data["end_date"] = validated_data["start_date"] + relativedelta(months=12)

        validated_data["booked_plans"] = plan 
        return Payment_plans.objects.create(amount = plan.price, **validated_data)
    
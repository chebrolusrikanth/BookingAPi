from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'client_name', 'client_email', 'booked_at', 'class_id']

    def validate(self, data):
        try:
            fitness_class = FitnessClass.objects.get(id=data['class_id'])
        except FitnessClass.DoesNotExist:
            raise serializers.ValidationError("Class ID does not exist.")

        if fitness_class.datetime < timezone.now():
            raise serializers.ValidationError("Cannot book a past class.")

        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No slots available.")

        return data

    def create(self, validated_data):
        fitness_class = FitnessClass.objects.get(id=validated_data['class_id'])
        fitness_class.available_slots -= 1
        fitness_class.save()
        return Booking.objects.create(
            fitness_class=fitness_class,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email']
        )

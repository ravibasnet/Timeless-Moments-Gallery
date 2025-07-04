from rest_framework import serializers
from .models import BookingSession, AvailableSlot
from django.contrib.auth import get_user_model

User = get_user_model()

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = ['id', 'date', 'max_sessions']

class BookingSessionSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    dates = serializers.JSONField(required=True)
    
    class Meta:
        model = BookingSession
        fields = '__all__'
    
    def validate(self, data):
        # Check if all required fields are present
        required_fields = ['session_type', 'dates', 'duration', 'location', 'client_name', 'client_email']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")
        
        # Validate dates is an array
        if not isinstance(data['dates'], list):
            raise serializers.ValidationError("dates must be an array")
        
        # If client is not provided, try to use a default user
        if 'client' not in data:
            default_user = User.objects.first()
            if default_user:
                data['client'] = default_user
        
        return data

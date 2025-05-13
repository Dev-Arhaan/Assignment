from rest_framework import serializers
from .models import Reminder
import datetime

class ReminderSerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        write_only=True,
        input_formats=["%Y-%m-%d", "iso-8601"],
        error_messages={
            "invalid": "Date must be in YYYY-MM-DD format.",
            "required": "Date is required."
        }
    )
    time = serializers.TimeField(
        write_only=True,
        input_formats=["%H:%M", "%H:%M:%S", "iso-8601"],
        error_messages={
            "invalid": "Time must be in HH:MM format.",
            "required": "Time is required."
        }
    )

    class Meta:
        model = Reminder
        fields = ['id', 'date', 'time', 'reminder_datetime', 'message', 'reminder_method', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reminder_datetime']

    def validate(self, data):
        input_date = data.get('date')
        input_time = data.get('time')
        message = data.get('message')
        reminder_method = data.get('reminder_method')

        # Validate presence
        if not input_date:
            raise serializers.ValidationError({"date": "Date is required."})
        if not input_time:
            raise serializers.ValidationError({"time": "Time is required."})
        if not message:
            raise serializers.ValidationError({"message": "Message cannot be empty."})
        if not reminder_method:
            raise serializers.ValidationError({"reminder_method": "Reminder method is required."})

        # Combine date and time
        try:
            combined_datetime = datetime.datetime.combine(input_date, input_time)
        except Exception:
            raise serializers.ValidationError("Invalid date and time combination.")

        # Validate that datetime is in the future
        if combined_datetime <= datetime.datetime.now():
            raise serializers.ValidationError("Reminder date and time must be in the future.")

        # Validate reminder method (redundant, but explicit)
        allowed_methods = dict(Reminder.REMINDER_METHOD_CHOICES).keys()
        if reminder_method not in allowed_methods:
            raise serializers.ValidationError({"reminder_method": f"Invalid method. Choose from: {', '.join(allowed_methods)}"})

        data['reminder_datetime'] = combined_datetime
        return data

    def create(self, validated_data):
        # Clean up date and time fields before saving
        validated_data.pop('date', None)
        validated_data.pop('time', None)
        return super().create(validated_data)

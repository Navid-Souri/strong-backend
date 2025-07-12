# progress_tracking/serializers.py
from rest_framework import serializers
from .models import DailyMood, WeightLog, PRRecord, DailyWaterLog # Removed WaterIntake
from accounts.serializers import UserSerializer
from workouts.serializers import ExerciseSerializer # To serialize Exercise details for PRRecord

class DailyMoodSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DailyMood
        fields = '__all__'
        read_only_fields = ['user']

    def validate_mood_rating(self, value): # Changed from mood_score to mood_rating
        if value < 1 or value > 5:
            raise serializers.ValidationError("Mood rating must be between 1 and 5.")
        return value

class WeightLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WeightLog
        fields = '__all__'
        read_only_fields = ['user']

class PRRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    exercise = ExerciseSerializer(read_only=True) # Display exercise details

    class Meta:
        model = PRRecord
        fields = '__all__'
        read_only_fields = ['user']

class DailyWaterLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Ensure user is read-only and set by view

    class Meta:
        model = DailyWaterLog
        fields = '__all__'
        read_only_fields = ['user'] # user will be set in ViewSet

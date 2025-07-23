from rest_framework import serializers
from django.db import transaction
from .models import Exercise, WorkoutPlan, WorkoutPlanExercise
from accounts.serializers import UserSerializer


class WorkoutPlanExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutPlanExercise
        fields = [
            'id', 'exercise', 'exercise_name', 'order',
            'default_sets', 'default_reps', 'default_weight_kg',
            'default_distance_km', 'default_time_seconds',
            'default_rpe', 'default_rest_seconds', 'default_notes'
        ]
        extra_kwargs = {
            'exercise': {'write_only': True, 'required': True},  # exercise ID must be provided
        }


class WorkoutPlanSerializer(serializers.ModelSerializer):
    # Write-only for creating/updating nested exercises
    exercises_details = WorkoutPlanExerciseSerializer(many=True, required=False, write_only=True)
    # Read-only for showing nested exercises
    exercises = WorkoutPlanExerciseSerializer(source='workoutplanexercise_set', many=True, read_only=True)

    created_by = UserSerializer(read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = '__all__'  # includes exercises_details and exercises

    @transaction.atomic
    def create(self, validated_data):
        exercises_details_data = validated_data.pop('exercises_details', [])
        user = self.context['request'].user

        workout_plan = WorkoutPlan.objects.create(created_by=user, **validated_data)

        for exercise_detail in exercises_details_data:
            exercise_id = exercise_detail.pop('exercise')
            exercise_instance = Exercise.objects.get(id=exercise_id)
            WorkoutPlanExercise.objects.create(
                workout_plan=workout_plan,
                exercise=exercise_instance,
                **exercise_detail
            )

        return workout_plan

    @transaction.atomic
    def update(self, instance, validated_data):
        exercises_details_data = validated_data.pop('exercises_details', None)

        # Update basic fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()

        if exercises_details_data is not None:
            # Get current exercises linked to this plan
            existing_wpe_ids = set(instance.workoutplanexercise_set.values_list('id', flat=True))

            for exercise_detail in exercises_details_data:
                exercise_id = exercise_detail.pop('exercise')
                exercise_instance = Exercise.objects.get(id=exercise_id)

                # Update or create the WorkoutPlanExercise
                wpe_instance, created = WorkoutPlanExercise.objects.update_or_create(
                    workout_plan=instance,
                    exercise=exercise_instance,
                    defaults=exercise_detail
                )

                if not created:
                    # If updated, remove from the set (means still exists)
                    existing_wpe_ids.discard(wpe_instance.id)

            # Delete old exercises that were not included in the new list
            WorkoutPlanExercise.objects.filter(id__in=existing_wpe_ids).delete()

        return instance

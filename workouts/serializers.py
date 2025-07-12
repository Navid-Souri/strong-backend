# workouts/serializers.py
from rest_framework import serializers
from .models import Exercise, WorkoutPlan, WorkoutPlanExercise, WorkoutSession, Set, UserWorkoutPlanAssignment
from accounts.serializers import UserSerializer 

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__' 

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
        # Make exercise writable when creating/updating WorkoutPlanExercise directly
        # but read_only when nested within WorkoutPlanSerializer (handled by create/update methods)
        extra_kwargs = {
            'exercise': {'write_only': True, 'required': True}, # Ensure exercise ID is provided
        }

class WorkoutPlanSerializer(serializers.ModelSerializer):
    # This field will be used for nested creation/update of WorkoutPlanExercise instances
    exercises_details = WorkoutPlanExerciseSerializer(many=True, required=False, write_only=True)
    
    # This field is for reading (displaying) exercises associated with the plan
    exercises = WorkoutPlanExerciseSerializer(source='workoutplanexercise_set', many=True, read_only=True)
    
    created_by = UserSerializer(read_only=True) 

    class Meta:
        model = WorkoutPlan
        fields = '__all__' # Includes 'exercises_details' for writing and 'exercises' for reading

    def create(self, validated_data):
        exercises_details_data = validated_data.pop('exercises_details', [])
        workout_plan = WorkoutPlan.objects.create(created_by=self.context['request'].user, **validated_data)
        
        for exercise_detail in exercises_details_data:
            exercise_id = exercise_detail.pop('exercise') # Get the Exercise instance
            WorkoutPlanExercise.objects.create(workout_plan=workout_plan, exercise=exercise_id, **exercise_detail)
        
        return workout_plan

    def update(self, instance, validated_data):
        exercises_details_data = validated_data.pop('exercises_details', None)

        # Update WorkoutPlan fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()

        if exercises_details_data is not None:
            # Handle nested WorkoutPlanExercise updates/creations/deletions
            # This is a more complex logic for updates, often involving comparing existing vs. new
            # For simplicity, this example will only add new ones or update existing ones by exercise+plan.
            # A full implementation might require deleting old ones not in the new list.

            # Get existing WorkoutPlanExercise instances for this plan
            existing_wpe_ids = set(instance.workoutplanexercise_set.values_list('exercise_id', flat=True))
            
            for exercise_detail in exercises_details_data:
                exercise_instance = exercise_detail.pop('exercise')
                order = exercise_detail.get('order')

                # Check if this WorkoutPlanExercise already exists for this plan and exercise
                wpe_instance, created = WorkoutPlanExercise.objects.update_or_create(
                    workout_plan=instance,
                    exercise=exercise_instance,
                    defaults={**exercise_detail, 'order': order} # Update all fields
                )
                if not created:
                    # If it was updated, remove its exercise_id from the set of existing ones
                    existing_wpe_ids.discard(exercise_instance.id)
            
            # Delete any WorkoutPlanExercise instances that were not in the new list
            # (This part is crucial if you want to allow removal of exercises from a plan during update)
            # WorkoutPlanExercise.objects.filter(workout_plan=instance, exercise_id__in=existing_wpe_ids).delete()


        return instance


class SetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    
    class Meta:
        model = Set
        fields = '__all__'
        extra_kwargs = {
            'workout_session': {'read_only': True},
            'load_kg': {'read_only': True}, 
        }

    def validate_rpe(self, value):
        if value is not None and (value < 1 or value > 10):
            raise serializers.ValidationError("RPE باید بین ۱ تا ۱۰ باشد.")
        return value

    def validate(self, data):
        metrics = ['reps', 'weight_kg', 'distance_km', 'time_seconds']
        if not any(field in data for field in metrics):
            raise serializers.ValidationError("حداقل یکی از فیلدهای تعداد تکرار، وزن، مسافت یا زمان باید پر شود.")
        return data


class WorkoutSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    sets = SetSerializer(many=True, read_only=True) 

    class Meta:
        model = WorkoutSession
        fields = '__all__'

class UserWorkoutPlanAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    workout_plan = WorkoutPlanSerializer(read_only=True) 
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = UserWorkoutPlanAssignment
        fields = '__all__'

from django.contrib import admin
from .models import Exercise, WorkoutPlan, WorkoutPlanExercise, WorkoutSession, Set, UserWorkoutPlanAssignment

# First define the inline class
class WorkoutPlanExerciseInline(admin.TabularInline):
    model = WorkoutPlanExercise
    extra = 1
    raw_id_fields = ['exercise']
    fields = ['exercise', 'order', 'default_sets', 'default_reps', 'default_weight_kg']

# Then define the admin class that uses it
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_public']
    list_filter = ['is_public']
    search_fields = ['name', 'description']
    raw_id_fields = ['created_by']
    inlines = [WorkoutPlanExerciseInline]  # Now this will work

# Register other models
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_cardio']
    list_filter = ['is_cardio']
    search_fields = ['name']

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'workout_plan', 'duration_minutes']
    list_filter = ['date', 'user']
    raw_id_fields = ['user', 'workout_plan']
    date_hierarchy = 'date'

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['workout_session', 'exercise', 'set_number', 'reps', 'weight_kg']
    list_filter = ['exercise']
    raw_id_fields = ['workout_session', 'exercise']

@admin.register(UserWorkoutPlanAssignment)
class UserWorkoutPlanAssignmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_plan', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']
    raw_id_fields = ['user', 'workout_plan', 'assigned_by']
    date_hierarchy = 'start_date'

# Finally register the WorkoutPlan with its admin class
admin.site.register(WorkoutPlan, WorkoutPlanAdmin)
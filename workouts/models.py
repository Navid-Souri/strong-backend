# workouts/models.py
from django.db import models
from core.models import TimestampedModel
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Exercise(TimestampedModel):
    """Model for defining exercises (e.g., Squat, Bench Press)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Exercise Name")
    description = models.TextField(blank=True, verbose_name="Description")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video Link")
    is_cardio = models.BooleanField(default=False, verbose_name="Is Cardio?")

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

    def __str__(self):
        return self.name

class WorkoutPlanExercise(TimestampedModel):
    """Intermediate model for Many-to-Many relationship between WorkoutPlan and Exercise
    Also stores default details for each exercise within this plan."""
    workout_plan = models.ForeignKey('WorkoutPlan', on_delete=models.CASCADE, verbose_name="Workout Plan")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="Exercise")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    default_sets = models.PositiveIntegerField(blank=True, null=True, verbose_name="Default Sets")
    default_reps = models.PositiveIntegerField(blank=True, null=True, verbose_name="Default Reps")
    default_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Default Weight (kg)")
    default_distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Default Distance (km)")
    default_time_seconds = models.PositiveIntegerField(blank=True, null=True, verbose_name="Default Time (seconds)")
    default_rpe = models.PositiveSmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Default RPE (1-10)"
    )
    default_rest_seconds = models.PositiveIntegerField(blank=True, null=True, verbose_name="Default Rest Time (seconds)")
    default_notes = models.TextField(blank=True, verbose_name="Default Notes")

    class Meta:
        unique_together = ('workout_plan', 'exercise')
        ordering = ['order']
        verbose_name = "Exercise in Plan"
        verbose_name_plural = "Exercises in Plans"

    def __str__(self):
        return f"{self.workout_plan.name} - {self.exercise.name} (Order: {self.order})"

class WorkoutPlan(TimestampedModel):
    """Model for defining workout plans (e.g., Full Body Plan)"""
    name = models.CharField(max_length=150, verbose_name="Workout Plan Name")
    description = models.TextField(blank=True, verbose_name="Plan Description")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_workout_plans', verbose_name="Created By")
    is_public = models.BooleanField(default=False, verbose_name="Is Public?")
    exercises = models.ManyToManyField(Exercise, through='WorkoutPlanExercise', related_name='workout_plans', verbose_name="Exercises")

    class Meta:
        verbose_name = "Workout Plan"
        verbose_name_plural = "Workout Plans"

    def __str__(self):
        # Corrected: WorkoutPlan's __str__ should use its own name
        return self.name

# CORRECTED: WorkoutSession is now a top-level class, not nested
class WorkoutSession(TimestampedModel):
    """Model for a workout session completed by a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_sessions', verbose_name="User")
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Workout Plan (Optional)")
    date = models.DateField(verbose_name="Session Date")
    notes = models.TextField(blank=True, verbose_name="Notes")
    duration_minutes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duration (minutes)")

    class Meta:
        verbose_name = "Workout Session"
        verbose_name_plural = "Workout Sessions"
        ordering = ['-date', '-created_at']

    def __str__(self):
        # This __str__ method is correct for WorkoutSession
        return f"{self.user.username}'s workout on {self.date}"

class Set(TimestampedModel):
    """Model for each set performed in a workout session"""
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets', verbose_name="Workout Session")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets_performed', verbose_name="Exercise") # Added related_name
    set_number = models.PositiveIntegerField(verbose_name="Set Number")
    reps = models.PositiveIntegerField(blank=True, null=True, verbose_name="Reps")
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Weight (kg)")
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Distance (km)")
    time_seconds = models.PositiveIntegerField(blank=True, null=True, verbose_name="Time (seconds)")
    rpe = models.PositiveSmallIntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="RPE (1-10)"
    )
    load_kg = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Total Load (kg)"
    )
    rest_seconds = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Rest Time (seconds)"
    )
    notes = models.TextField(blank=True, verbose_name="Set Notes")

    class Meta:
        verbose_name = "Set"
        verbose_name_plural = "Sets"
        ordering = ['set_number']

    def __str__(self):
        return f"{self.workout_session.user.username} - {self.exercise.name} - Set {self.set_number}"

    def save(self, *args, **kwargs):
        if self.weight_kg is not None and self.reps is not None:
            self.load_kg = self.weight_kg * self.reps
        else:
            self.load_kg = None
        super().save(*args, **kwargs)

class UserWorkoutPlanAssignment(TimestampedModel):
    """Model for assigning workout plans to users (by a coach)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_workout_plans', verbose_name="User")
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='assigned_users', verbose_name="Workout Plan")
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments_made', verbose_name="Assigned By Coach")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    class Meta:
        unique_together = ('user', 'workout_plan', 'start_date')
        verbose_name = "User Workout Plan Assignment"
        verbose_name_plural = "User Workout Plan Assignments"

    def __str__(self):
        return f"{self.user.username} assigned to {self.workout_plan.name}"

# Daily Mood Model and Water Intake Model removed from here.
# They will be defined in progress_tracking/models.py

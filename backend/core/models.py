from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    PERSONALITY_CHOICES = [
        ('INTJ', 'INTJ - Architect'),
        ('INTP', 'INTP - Logician'),
        ('ENTJ', 'ENTJ - Commander'),
        ('ENTP', 'ENTP - Debater'),
        ('INFJ', 'INFJ - Advocate'),
        ('INFP', 'INFP - Mediator'),
        ('ENFJ', 'ENFJ - Protagonist'),
        ('ENFP', 'ENFP - Campaigner'),
        ('ISTJ', 'ISTJ - Logistician'),
        ('ISFJ', 'ISFJ - Defender'),
        ('ESTJ', 'ESTJ - Executive'),
        ('ESFJ', 'ESFJ - Consul'),
        ('ISTP', 'ISTP - Virtuoso'),
        ('ISFP', 'ISFP - Adventurer'),
        ('ESTP', 'ESTP - Entrepreneur'),
        ('ESFP', 'ESFP - Entertainer'),
    ]
    
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    personality_type = models.CharField(
        max_length=4,
        choices=PERSONALITY_CHOICES,
        blank=True
    )
    # New fields for enhanced user preferences
    personality_details = models.JSONField(default=dict, blank=True)  # Store detailed personality test results
    available_time = models.PositiveIntegerField(help_text="Available minutes per day", default=60)
    budget_preference = models.CharField(
        max_length=20,
        choices=[
            ('LOW', '$0-50'),
            ('MEDIUM', '$50-200'),
            ('HIGH', '$200+')
        ],
        default='MEDIUM'
    )
    profile_completed = models.BooleanField(default=False)
    coins = models.PositiveIntegerField(default=0)
    exp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Hobby(models.Model):
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced')
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='BEGINNER'
    )
    time_commitment = models.PositiveIntegerField(help_text="Required minutes per day")
    price_range = models.CharField(max_length=50)
    required_equipment = models.JSONField(default=list, blank=True)
    minimum_age = models.PositiveIntegerField(default=0)
    related_hobbies = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', related_name='hobbies')
    
    class Meta:
        verbose_name_plural = "hobbies"

class HobbyTasting(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='tastings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=15)
    equipment_needed = models.JSONField(default=list, blank=True)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Challenge(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='challenges')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    description = models.TextField()
    reward = models.PositiveIntegerField()  # in coins
    progress = models.PositiveIntegerField(default=0)
    target = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()

class UserHobby(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FAVORITE = 'favorite', 'Favorite'
        COMPLETED = 'completed', 'Completed'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hobbies')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='user_hobbies')
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.TextField(blank=True)  # Personal notes about the hobby
    resources_links = models.JSONField(default=list, blank=True)  # To store useful links
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

class HobbyResource(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50)  # tutorial, inspiration, material
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class RouletteHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roulette_history')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    suggested_at = models.DateTimeField(auto_now_add=True)
    was_accepted = models.BooleanField(default=False)
    coins_spent = models.PositiveIntegerField(default=0)  # If user paid for early access

class SystemSettings(models.Model):
    """Global settings for prices and timings"""
    roulette_cooldown_hours = models.PositiveIntegerField(default=24)
    roulette_early_price = models.PositiveIntegerField(default=50)  # coins cost
    new_hobby_activation_price = models.PositiveIntegerField(default=100)
    hobby_deletion_price = models.PositiveIntegerField(default=0)  # free
    
    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
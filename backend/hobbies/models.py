from django.db import models
from core.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

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
    tags = models.ManyToManyField(Tag, related_name='hobbies')
    
    class Meta:
        verbose_name_plural = "hobbies"

class UserHobby(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        FAVORITE = 'favorite', 'Favorite'
        COMPLETED = 'completed', 'Completed'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hobbies')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='user_hobbies')
    status = models.CharField(max_length=10, choices=Status.choices)
    notes = models.TextField(blank=True)
    resources_links = models.JSONField(default=list, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

class HobbyTasting(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='tastings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=15)
    equipment_needed = models.JSONField(default=list, blank=True)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
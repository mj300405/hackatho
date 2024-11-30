from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    
    # Required fields
    age = models.PositiveIntegerField(null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    personality_type = models.CharField(
        max_length=4,
        choices=PERSONALITY_CHOICES,
        null=False,
        blank=False
    )
    coins = models.PositiveIntegerField(default=0, null=False, blank=False)
    exp = models.PositiveIntegerField(default=0, null=False, blank=False)
    
    # Optional fields
    personality_details = models.JSONField(default=dict, blank=True, null=True)
    available_time = models.PositiveIntegerField(
        help_text="Available minutes per day",
        default=60,
        null=True,
        blank=True
    )
    budget_preference = models.CharField(
        max_length=20,
        choices=[
            ('LOW', '$0-50'),
            ('MEDIUM', '$50-200'),
            ('HIGH', '$200+')
        ],
        default='MEDIUM',
        null=True,
        blank=True
    )
    
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class SystemSettings(models.Model):
    roulette_cooldown_hours = models.PositiveIntegerField(default=24)
    roulette_early_price = models.PositiveIntegerField(default=50)
    new_hobby_activation_price = models.PositiveIntegerField(default=100)
    hobby_deletion_price = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'

    @classmethod
    def get_settings(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
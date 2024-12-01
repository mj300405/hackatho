from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

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

    def can_use_roulette_free(self):
        """
        Checks if the user can use the roulette for free based on their last usage.
        Returns True if enough time has passed since last usage, False otherwise.
        """
        settings = SystemSettings.get_settings()
        cooldown_period = timedelta(hours=settings.roulette_cooldown_hours)
        
        # Get the user's latest roulette history
        latest_spin = self.roulette_history.order_by('-suggested_at').first()
        
        if not latest_spin:
            # If user has never used the roulette, they can use it for free
            return True
            
        # Check if enough time has passed since last usage
        time_passed = timezone.now() - latest_spin.suggested_at
        return time_passed >= cooldown_period
    
    def get_roulette_cost(self):
        """
        Returns the cost in coins to use the roulette before the cooldown period ends.
        """
        settings = SystemSettings.get_settings()
        return settings.roulette_early_price if not self.can_use_roulette_free() else 0
    
    def get_next_free_roulette_time(self):
        """
        Returns the datetime when the user can next use the roulette for free.
        """
        latest_spin = self.roulette_history.order_by('-suggested_at').first()
        if not latest_spin:
            return timezone.now()
            
        settings = SystemSettings.get_settings()
        return latest_spin.suggested_at + timedelta(hours=settings.roulette_cooldown_hours)


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
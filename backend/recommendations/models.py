from django.db import models
from core.models import User
from hobbies.models import Hobby

class RouletteHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roulette_history')
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    suggested_at = models.DateTimeField(auto_now_add=True)
    was_accepted = models.BooleanField(default=False)
    coins_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s roulette - {self.hobby.name}"
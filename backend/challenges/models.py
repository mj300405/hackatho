from django.db import models
from core.models import User
from hobbies.models import Hobby

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

    def __str__(self):
        return f"Challenge for {self.hobby.name} - {self.user.username}"
from django.db import models
from api.models import User
from properties.models import Property


class Review(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Store the user but don't expose on the frontend
    comment = models.TextField()
    rating = models.IntegerField()  # Star rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.property.name}"

    class Meta:
        unique_together = [
            "property",
            "user",
        ]  # Prevent users from reviewing the same property multiple times

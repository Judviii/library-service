from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        SOFT = "SOFT", "Soft"
        HARD = "HARD", "Hard"

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=64, unique=True)
    cover = models.CharField(
        max_length=4,
        choices=CoverChoices.choices,
        default=CoverChoices.SOFT,
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Daily fee (in $USD)",
    )

    def __str__(self):
        return f"{self.title}, {self.author}"

    class Meta:
        unique_together = ("title", "author", "cover")
        ordering = ["title"]

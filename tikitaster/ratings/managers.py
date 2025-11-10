from django.db import models
from django.db.models import Avg

class DrinkQuerySet(models.QuerySet):
    def with_average_ratings(self):
        return self.annotate(
            # Define all the aggregate fields here once
            avg_overall=Avg('ratings__overall_rating'),
            avg_taste=Avg('ratings__taste_rating'),
            avg_presentation=Avg('ratings__presentation_rating')
        )
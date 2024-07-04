from django.db import models


class Activities(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    date_time = models.DateTimeField(null=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    daring_rating = models.IntegerField()
    completed = models.BooleanField()
    planned = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name

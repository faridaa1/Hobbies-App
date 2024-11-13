from django.db import models

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class Hobby(models.Model):
    """Defines Hobby model with name attribute."""
    name = models.CharField(blank=False, null=False, unique=True, max_length=255)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        """String representation of Hobby object."""
        return f"{self.name}: {self.description}"


# I forgot I didn't need to add this so you can use this for the M:M or change/delete it
# HOBBY_LEVEL = [
#     ('Beginner', 'Beginner'),
#     ('Intermediate', 'Intermediate'),
#     ('Advanced', 'Advanced')
# ]
# level = models.CharField(blank=False, null=False, choices=HOBBY_LEVEL, default='Beginner', max_length=12)

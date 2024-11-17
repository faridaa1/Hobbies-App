from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class Hobby(models.Model):
    """Defines Hobby model with relevant attributes and methods."""
    name = models.CharField(blank=False, null=False, unique=True, max_length=255)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        """String representation of Hobby object."""
        return f"{self.name}: {self.description}"
    
    def as_dict(self):
        """Dictionary representation of Hobby object."""
        return {
            'hobby_id': self.id,
            'hobby_name': self.name,
            'hobby_description': self.description
        }


class CustomUser(AbstractUser):
    """Defines the custom user model"""
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', blank=True, related_name="users")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    """ resolve clashes with the default reverse relations """
    groups = models.ManyToManyField(
        Group, 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, 
        blank=True
    )
    
    """Returns the username as a string"""
    def __str__(self):
        return self.username
    
    def as_dict(self):
        """ dictionary representation of the CustomUser object. """
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "hobbies": [hobby.name for hobby in self.hobbies.all()],
            "profile_picture": self.profile_picture.url if self.profile_picture else None,
        }


class UserHobby(models.Model):
    """ The through model to represent ManyToMany relationship between user and hobby """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    """ Choice field representing the user's skill level in the hobby """
    HOBBY_LEVEL = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    level = models.CharField(blank=False, null=False, choices=HOBBY_LEVEL, default='Beginner', max_length=12)
    startDate = models.DateField(null=False, blank=False, default=now)

    """ return a string repsentation for user hobbies """
    def __str__(self):
        return f"{self.user.username} - {self.hobby.name}({self.level})"
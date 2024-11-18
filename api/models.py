from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now


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
    """Defines the custom user model."""
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', blank=True, related_name="users")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    """Resolve clashes with the default reverse relations."""
    groups = models.ManyToManyField(
        Group, 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, 
        blank=True
    )
    
    def __str__(self):
        """Returns the username as a string."""
        return self.username
    
    def as_dict(self):
        """Dictionary representation of the CustomUser object."""
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "hobbies": [hobby.name for hobby in self.hobbies.all()],
            "profile_picture": self.profile_picture.url if self.profile_picture else None,
        }

class Friendship(models.Model):
    """The through model to represent ManyToMany relationship between User and User."""

class UserHobby(models.Model):
    """The through model to represent ManyToMany relationship between User and Hobby."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    """Choice field representing the user's skill level in the hobby."""
    HOBBY_LEVEL = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    level = models.CharField(blank=False, null=False, choices=HOBBY_LEVEL, default='Beginner', max_length=12)
    start_date = models.DateField(null=False, blank=False, default=now)

    def __str__(self):
        """Return a string repsentation for user hobbies."""
        return f"{self.user.username} - {self.hobby.name}({self.level})"
    
    def as_dict(self):
        """Defining dictionary representation of UserHobby."""
        return {
            "user" : self.user.id,
            "hobby" : self.hobby.id,
            "level" : self.level,
            "start_date" : self.start_date
        }
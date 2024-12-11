from typing import Any
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.forms import ValidationError
from django.utils.timezone import now


class Hobby(models.Model):
    """Defines Hobby model with relevant attributes and methods."""
    name = models.CharField(blank=False, null=False, unique=True, max_length=255)
    description = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        """String representation of Hobby object."""
        return f"{self.name}: {self.description}"
    
    def as_dict(self) -> dict[str, Any]:
        """Dictionary representation of Hobby object."""
        return {
            'hobby_id': self.id,
            'hobby_name': self.name,
            'hobby_description': self.description
        }


class CustomUser(AbstractUser):
    """Defines the custom user model."""
    name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=False)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=False, blank=True)
    hobbies = models.ManyToManyField(Hobby, through='UserHobby', blank=True, related_name="users")
    friends = models.ManyToManyField(to='self', symmetrical=True, through='Friendship', blank=True)

    """Resolve clashes with the default reverse relations."""
    groups = models.ManyToManyField(
        Group, 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, 
        blank=True
    )
    
    def __str__(self) -> str:
        """Returns the username as a string."""
        return self.username
    
    def as_dict(self) -> dict[str, Any]:
        """Dictionary representation of the CustomUser object."""
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "hobbies": [hobby.as_dict() for hobby in self.hobbies.all()],
            "friends": [friendship.as_dict(self) for friendship in Friendship.objects.filter(Q(user1=self) | Q(user2=self))],
            "profile_picture": self.profile_picture.url if self.profile_picture else None,
        }


class Friendship(models.Model):
    """The through model to represent ManyToMany relationship between User and User."""
    user1 = models.ForeignKey(CustomUser, related_name="sent_requests", on_delete=models.CASCADE)
    user2 = models.ForeignKey(CustomUser, related_name="received_requests", on_delete=models.CASCADE)

    def clean(self):
        """Preventing self-friendships and reverse friendships (duplicate)."""
        if self.user1 == self.user2:
            raise ValidationError("You cannot be friends with yourself")
        if Friendship.objects.filter(user1=self.user2, user2=self.user1).exists():
            raise ValidationError("This friendship already exists")
        
    STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    status = models.CharField(blank=False, null=False, choices=STATUS, default='Pending', max_length=12)

    def __str__(self) -> str:
        """Return a string repsentation for Friendship."""
        return f"{self.user1} & {self.user2}: {self.status}"
    
    def as_dict(self, current_user) -> dict[str, Any]:
        user: CustomUser
        sent:bool = False
        if self.user1 == current_user:
            user = self.user2
            sent = True
        else:
            user = self.user1

        """Defining dictionary representation of Friendship."""
        return {
            "id" : self.id,
            "user_name" : user.name,
            "user_profile_picture" : user.profile_picture.url if user.profile_picture else None,
            "status" : self.status,
            "sent" : sent
        }

    class Meta:
        """Preventing duplicate friendships."""
        constraints = [
            models.UniqueConstraint(fields=['user1','user2'], name='unique_friendship')
        ]


class UserHobby(models.Model):
    """The through model to represent ManyToMany relationship between User and Hobby."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    """Choice field representing the User's skill level in the Hobby."""
    HOBBY_LEVEL = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ]
    level = models.CharField(blank=False, null=False, choices=HOBBY_LEVEL, default='Beginner', max_length=12)
    start_date = models.DateField(null=False, blank=False, default=now)

    def __str__(self) -> str:
        """Return a string repsentation for User Hobbies."""
        return f"{self.user.username} - {self.hobby.name}({self.level})"
    
    def as_dict(self) -> dict[str, Any]:
        """Defining dictionary representation of UserHobby."""
        return {
            "user" : self.user.as_dict(),
            "hobby" : self.hobby.as_dict(),
            "level" : self.level,
            "start_date" : self.start_date
        }
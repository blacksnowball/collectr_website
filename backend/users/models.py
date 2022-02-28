"""
A file contains all the classes for users
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .extras import get_tokens

class CustomAccountManager(BaseUserManager):
    """
    A class used for representing the account manager
    """
    def create_superuser(self, email, username, password, **other_fields):
        """
        A method used for creating superuser
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        """
        A method used for creating normal user
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A class used for representing system user
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500,
        default = "A bio hasn't been added yet.")
    # staff = Curator (edits items/collections, other people's reputations
    is_staff = models.BooleanField(default=False)
    # activated at email validation only, not at registration.
    is_active = models.BooleanField(default=False)
    picture = models.ImageField(upload_to="uploads/", blank=True)
    # user_collections = models.ManyToManyField("UserCollection")
    # the user collection items need to manually be added

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username} ({self.id})'

    def has_perm(self, perm, obj=None):
        """
        A method used to check if the user has permission
        """
        return True

    def tokens(self):
        """
        A method used to get the token of user
        """
        return get_tokens(self)

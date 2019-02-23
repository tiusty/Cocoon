from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.utils.text import slugify
from cocoon.houseDatabase.models import RentDatabaseModel
# Import third party libraries
import hashlib


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, is_superuser, is_admin, **extra_fields):
        """
        Creates and saves a User with the given email and password
        :param email:
        :param password:
        :param is_staff:
        :param is_superuser:
        :param extra_fields:
        :return:
        """

        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True,
                          is_superuser=is_superuser, is_admin=is_admin,
                          last_login=now,
                          joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class
    """
    email = models.EmailField('email address', unique=True, db_index=True)
    joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_broker = models.BooleanField(default=False)
    is_hunter = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(blank=True, max_length=200)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def date_joined(self):
        """
        Needed by intercom. Intercom looks for date_joined field
        """
        return self.joined

    def has_perm(self, perm, obj=None):
        "Does the user have a spcific premission?"
        # Simpliest possible answer: yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Defines the Manager for the custom User model
class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, related_name="userProfile", on_delete=models.CASCADE, default='none')
    url = models.SlugField(max_length=100, default="")

    def generate_slug(self):
        # Create the unique string that will be hashed
        # Multiple things are added so people can't reverse hash the id
        hashable_string = "{0}{1}{2}".format(self.user.phone_number[:2], self.user.id, self.user.joined,)

        # Create the md5 object
        m = hashlib.md5()

        # Add the string to the hash function
        m.update(hashable_string.encode('utf-8'))

        # Now return the has has the url
        return slugify(m.hexdigest())

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.generate_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.get_short_name()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
            UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=MyUser)
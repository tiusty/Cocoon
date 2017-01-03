from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
# Create your models here.


class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, is_superuser, is_admin,**extra_fields):
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
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)


    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

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
    test = models.CharField(max_length=200)
    def __str__(self):
        return self.user.get_short_name()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
            UserProfile.objects.create(user=instance, test="Please enter something")


post_save.connect(create_user_profile, sender=MyUser)
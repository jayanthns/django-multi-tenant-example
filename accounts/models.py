from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255
    )
    # notice the absence of a 'Password field' , that's built in.
    created_on = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # A SUPER USER
    last_login = models.DateTimeField(null=True, blank=True)
    forgot_password_token = models.CharField(max_length=120, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password are required by default

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def staff(self):
        """Is the user a member of staff?"""
        return self.is_staff

    @property
    def superuser(self):
        """Is the user a admin member?"""
        return self.is_superuser

    @property
    def active(self):
        """Is the user active?"""
        return self.is_active

    objects = AccountManager()


class Profile(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True
    )
    first_name = models.CharField(max_length=250, null=True, default="")
    last_name = models.CharField(max_length=250, null=True, default="")
    ph_number = models.CharField(max_length=15, null=True, default="")
    zipcode = models.CharField(max_length=10, null=True, default="")
    address1 = models.CharField(max_length=500, null=True, default="")
    address2 = models.CharField(max_length=500, null=True, default="")
    secondary_ph_number = models.CharField(max_length=15, null=True, default="")
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=50, null=True, default="")
    role = models.CharField(max_length=100, default='')

    def dob_value(self):
        return '' if not self.dob else self.dob.strftime("%d-%m-%Y")


class Team(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(sel):
        return self.name

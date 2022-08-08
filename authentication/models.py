from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email):
        account = self.model(email=self.normalize_email(email))
        pwd = get_random_string()
        account.set_password(pwd)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, password):
        account = self.create_user(
            email=self.normalize_email(email)
        )

        account.set_password(password)
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.active = True

        if account.is_superuser is not True:
            raise ValueError('Superuser must be assigned to Superuser=True')
        if account.is_admin is not True:
            raise ValueError('Superuser must be assigned to Admin=True')
        if account.is_staff is not True:
            raise ValueError('Superuser must be assigned to Staff=True')

        account.save(using=self._db)
        return account


class Account(AbstractBaseUser):

    name = models.CharField(default='User', max_length=80, null=True, blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        abstract = False

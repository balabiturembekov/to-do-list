from django.db import models
from django.contrib.auth.models import (
            AbstractBaseUser, BaseUserManager, 
            PermissionsMixin,
            )


class Token(models.Model):
    ''' Модель Токена для пользователя '''
    email = models.EmailField()
    uid = models.CharField(max_length=255)


class ListUserManager(BaseUserManager):
    ''' Менеджер пользователя '''
    def create_user(self, email):
        ''' Создать пользователя '''
        ListUser.objects.create(email=email)

    def create_super_user(self, email, password):
        ''' Создать супер пользователя '''
        self.create_user(email)


class ListUser(AbstractBaseUser, PermissionsMixin):
    ''' Модель пользователя списка '''
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['email', 'height']

    objects = ListUserManager()

    @property
    def is_staff(self):
        return self.email == 'turembekov@example.com'

    @property
    def is_active(self):
        return True


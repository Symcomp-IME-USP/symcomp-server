from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Link(models.Model):
    domain = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.domain

class Palestrante(models.Model):
    nome = models.CharField(max_length=255)
    ocupacao = models.CharField(max_length=255)
    biografia = models.TextField()
    email = models.EmailField()
    link_apresentacao = models.URLField()
    foto_url = models.URLField()
    foto_alt = models.CharField(max_length=255)
    links = models.ManyToManyField(Link, related_name="palestrantes")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("O email é obrigatório.")
        if not name:
            raise ValueError("O nome completo é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

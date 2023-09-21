from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    # Establece is_active en True por defecto para todos los usuarios
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set", blank=True
    )


class Entrenamiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class Ejercicio(models.Model):
    entrenamiento = models.ForeignKey(
        Entrenamiento, on_delete=models.CASCADE, related_name="ejercicios", null=True
    )
    # Otros campos del ejercicio
    nombre = models.CharField(max_length=200)
    repeticiones = models.CharField(max_length=200)
    peso = models.CharField(max_length=200)
    descanso = models.CharField(max_length=20, null=True, blank=True)
    comentarios = models.CharField(max_length=3000, null=True, blank=True)


class Plan(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="planes", null=True
    )
    nombre_entrenamiento = models.CharField(max_length=200, default="")
    fecha = models.CharField(max_length=20)
    hora_inicio = models.CharField(max_length=20, null=True, blank=True)
    hora_fin = models.CharField(max_length=20, null=True, blank=True)


class PersonalData(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="personal", null=True
    )
    peso = models.CharField(max_length=20, null=True, blank=True)
    altura = models.CharField(max_length=20, null=True, blank=True)
    edad = models.CharField(max_length=20, null=True, blank=True)
    objetivo = models.CharField(max_length=250, null=True, blank=True)
    genero = models.CharField(max_length=20, null=True, blank=True)

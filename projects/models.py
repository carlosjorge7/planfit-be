from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


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
    equipo = models.CharField(max_length=100, null=True, blank=True)
    one_rm = models.CharField(max_length=20, null=True, blank=True)
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


class Comida(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comidas", null=True
    )
    entrenamiento = models.ForeignKey(
        Entrenamiento, on_delete=models.CASCADE, related_name="comidas", null=True
    )
    desayuno = models.CharField(max_length=200, null=True, blank=True)
    comida = models.CharField(max_length=200, null=True, blank=True)
    merienda = models.CharField(max_length=200, null=True, blank=True)
    cena = models.CharField(max_length=200, null=True, blank=True)
    nutrientes = models.CharField(
        max_length=200, null=True, blank=True
    )  # carbohidratos, proteinas, lipidos, fibra, lacteos ..

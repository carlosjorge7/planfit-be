from rest_framework import serializers

from .models import User, Entrenamiento, Ejercicio, Plan, PersonalData, Comida


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["is_active"] = True
        user = User.objects.create_user(**validated_data)
        return user


class EntrenamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrenamiento
        fields = (
            "id",
            "usuario",
            "title",
            "tipo",
            "description",
        )


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = (
            "id",
            "entrenamiento",
            "nombre",
            "repeticiones",
            "peso",
            "equipo",
            "one_rm",
            "descanso",
            "comentarios",
        )


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "usuario",
            "nombre_entrenamiento",
            "fecha",
            "hora_inicio",
            "hora_fin",
        )


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalData
        fields = ("id", "usuario", "peso", "altura", "edad", "objetivo", "genero")


class ComidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comida
        fields = (
            "id",
            "usuario",
            "entrenamiento",
            "nombre",
            "desayuno",
            "comida",
            "merienda",
            "cena",
            "notas",
        )

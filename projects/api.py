from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Entrenamiento, Ejercicio, Plan, PersonalData, Comida
from .serializers import (
    UserSerializer,
    EntrenamientoSerializer,
    EjercicioSerializer,
    PlanSerializer,
    PersonalDataSerializer,
    ComidaSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q


# USER API
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


# Personalizo la clase TokenObtainPairView para que devuelva el id del usuario
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Si las credenciales son válidas y se generó el token de acceso,
        # agrega el ID del usuario a la respuesta
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data.get("username"))
            user_id = user.id
            response.data["user_id"] = user_id

        return response


# ENTRRENAMIENTO API
class EntrenamientoListCreateView(generics.ListCreateAPIView):
    serializer_class = EntrenamientoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

    # Filtro
    def get_queryset(self):
        user = self.request.user
        queryset = Entrenamiento.objects.filter(usuario=user)

        titles = self.request.query_params.get("title", None)

        if titles:
            # Divide la cadena de títulos en una lista
            titles_list = titles.split(",")
            # Crea una consulta Q OR para filtrar exactamente por una o varias posiciones del array
            queries = Q()
            for title in titles_list:
                queries |= Q(title=title)
            queryset = queryset.filter(queries)
        return queryset


class EntrenamientoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entrenamiento.objects.all()
    serializer_class = EntrenamientoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        # Eliminar todos los ejercicios asociados al entrenamiento
        Ejercicio.objects.filter(entrenamiento=instance).delete()

        # Eliminar todos los planes asociados al entrenamiento
        Plan.objects.filter(nombre_entrenamiento=instance.id).delete()

        # Finalmente, eliminar el entrenamiento
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# EJERCICIO API
class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer
    permission_classes = (IsAuthenticated,)

    # List ejercicios by entrenamiento
    def list(self, request, *args, **kwargs):
        entrenamiento_id = self.request.GET.get("entrenamiento")
        if entrenamiento_id:
            try:
                entrenamiento = Entrenamiento.objects.get(id=entrenamiento_id)
                ejercicios = entrenamiento.ejercicios.all()
                serializer = self.get_serializer(ejercicios, many=True)
                return Response(serializer.data)
            except Entrenamiento.DoesNotExist:
                return Response(
                    {"error": "Entrenamiento no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "Parámetro de entrenamiento faltante"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# PLAN API
class PlanListCreateView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

    # Get planes by user (No hace falta mandarle el id user: Viaja en el TOKEN)
    def get_queryset(self):
        user = self.request.user
        return Plan.objects.filter(usuario=user)


class PlanRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = (IsAuthenticated,)


# DATOS PERSONALES API
class PersonalDataListCreateView(generics.ListCreateAPIView):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

    # Get personal data by user (No hace falta mandarle el id user: Viaja en el TOKEN)
    def get_queryset(self):
        user = self.request.user
        return PersonalData.objects.filter(usuario=user)


class PersonalDataRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer
    permission_classes = (IsAuthenticated,)


# COMIDA API
class ComidaListCreateView(generics.ListCreateAPIView):
    queryset = Comida.objects.all()
    serializer_class = ComidaSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    # Get comidas by user (No hace falta mandarle el id user: Viaja en el TOKEN)
    def get_queryset(self):
        user = self.request.user
        return Comida.objects.filter(usuario=user)


class ComidaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comida.objects.all()
    serializer_class = ComidaSerializer
    permission_classes = (IsAuthenticated,)

from rest_framework import routers

from .api import EjercicioViewSet

router = routers.DefaultRouter()


router.register("ejercicios", EjercicioViewSet, "ejercicios")


urlpatterns = router.urls

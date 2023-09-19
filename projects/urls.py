from rest_framework import routers

from .api import ProjectViewSet, EjercicioViewSet

router = routers.DefaultRouter()

router.register("api/projects", ProjectViewSet, "projects")
router.register("ejercicios", EjercicioViewSet, "ejercicios")


urlpatterns = router.urls
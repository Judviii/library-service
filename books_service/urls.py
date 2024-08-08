from rest_framework import routers
from django.urls import path, include

from books_service.views import BookViewSet

router = routers.DefaultRouter()
router.register("", BookViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "books_service"

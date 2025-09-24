import logging

# Django core
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse

# Django REST Framework
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from .forms import SignUpForm

logger = logging.getLogger("tasks")


# ==============================================================================
# 1. Vistas de Interfaz (Renderizan templates HTML)
# ==============================================================================


def home_view(request):
    return render(request, "home.html")


def signup_view(request):
    """
    Maneja el registro de nuevos usuarios.
    Asigna is_staff=True para permitir el acceso a la API (IsAuthenticated).
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            login(request, user)
            logger.info(f"Nuevo usuario registrado: {user.username} (ID: {user.id})")
            return redirect(reverse("task_list"))
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required
def task_interface_view(request):
    return render(request, "task_list.html")


class CustomLoginView(BaseLoginView):
    """
    Extiende la vista de login base de Django para personalizar la redirección
    basada en el tipo de usuario.
    """

    def get_success_url(self):
        if self.request.user.is_superuser:
            logger.info(
                f"Superusuario logueado: {self.request.user.username}. Redirigido a admin."
            )
            return reverse("admin:index")
        else:
            logger.info(
                f"Usuario estándar logueado: {self.request.user.username}. Redirigido a task_list."
            )
            return reverse("task_list")


# ==============================================================================
# 2. Vistas de API (DRF)
# ==============================================================================


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    API View para LISTAR (GET) y CREAR (POST) tareas.
    Aplica filtros avanzados y autenticación.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = ["title", "description"]  # Búsqueda por contenido

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Asocia automáticamente la nueva tarea al usuario autenticado.
        serializer.save(user=self.request.user)
        logger.info(
            f"TAREA CREADA: '{serializer.instance.title}' por {self.request.user.username} (ID: {self.request.user.id})"
        )


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View para RECUPERAR (GET), ACTUALIZAR (PATCH/PUT) y ELIMINAR (DELETE) tareas individuales.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        task_title = instance.title
        user_info = self.request.user.username
        instance.delete()
        logger.warning(f"TAREA ELIMINADA: '{task_title}' por el usuario {user_info}.")

    def perform_update(self, serializer):
        # Comprobamos si el campo de estado fue modificado para loguear el cambio
        if "is_completed" in serializer.validated_data:
            new_status = (
                "COMPLETADA"
                if serializer.validated_data["is_completed"]
                else "PENDIENTE"
            )
            logger.info(
                f"TAREA ESTADO CAMBIADO: '{serializer.instance.title}' - Nuevo estado: {new_status} por {self.request.user.username}"
            )

        serializer.save()

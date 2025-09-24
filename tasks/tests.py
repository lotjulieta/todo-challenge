import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Task


class TaskModelTest(APITestCase):
    """
    Tests Unitarios para el modelo Task.
    Verifica la creación y los valores por defecto.
    """

    def setUp(self):
        # Crear un usuario para asociar la tarea
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.task = Task.objects.create(
            user=self.user, title="Test Task", description="This is a test description"
        )

    def test_task_creation(self):
        """Asegura que la tarea se crea con los valores correctos."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test description")
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.user, self.user)

    def test_task_string_representation(self):
        """Asegura que el método __str__ devuelve el título."""
        self.assertEqual(str(self.task), "Test Task")


# ---------------------------------------------------------------------------------


class TaskAPITest(APITestCase):
    """
    Tests de Integración para los endpoints de la API (DRF).
    Verifica la autenticación y el scope de usuario.
    """

    def setUp(self):
        # URLs de la API
        self.list_create_url = reverse("task-list-create")

        # Usuarios
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Tareas asociadas a User1
        self.task1 = Task.objects.create(
            user=self.user1, title="Tarea de User1", is_completed=False
        )
        self.task2 = Task.objects.create(
            user=self.user1, title="Otra Tarea de User1", is_completed=True
        )
        self.detail_url_user1 = reverse("task-detail", kwargs={"pk": self.task1.pk})

        # Tarea asociada a User2 (para verificar el scope)
        self.task_user2 = Task.objects.create(user=self.user2, title="Tarea de User2")
        self.detail_url_user2 = reverse(
            "task-detail", kwargs={"pk": self.task_user2.pk}
        )

    def test_unauthenticated_requests_are_denied(self):
        """Asegura que las peticiones sin autenticar fallan."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- PRUEBAS DE LISTADO (GET) ---

    def test_list_tasks_only_user_specific(self):
        """Asegura que User1 solo ve sus tareas y no las de User2."""
        self.client.login(username="user1", password="password123")
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Debe ver task1 y task2

        titles = [item["title"] for item in response.data]
        self.assertIn("Tarea de User1", titles)
        self.assertNotIn("Tarea de User2", titles)  # No debe ver la de User2

    # --- PRUEBAS DE CREACIÓN (POST) ---

    def test_create_task_associates_to_authenticated_user(self):
        """Asegura que al crear una tarea, se asocia automáticamente a User1."""
        self.client.login(username="user1", password="password123")
        data = {"title": "Nueva Tarea Creada", "description": "Descripción"}
        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)  # 3 existentes + 1 nueva

        # Verifica que la tarea está asociada a User1
        new_task = Task.objects.get(pk=response.data["id"])
        self.assertEqual(new_task.user, self.user1)

    # --- PRUEBAS DE ACTUALIZACIÓN (PATCH) ---

    def test_update_task_state_success(self):
        """Asegura que User1 puede marcar su tarea como completada."""
        self.client.login(username="user1", password="password123")
        data = {"is_completed": True}
        response = self.client.patch(self.detail_url_user1, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Task.objects.get(pk=self.task1.pk).is_completed)

    def test_update_task_of_other_user_denied(self):
        """Asegura que User1 NO puede actualizar la tarea de User2."""
        self.client.login(username="user1", password="password123")
        data = {"title": "Intento de Hackeo"}
        response = self.client.patch(self.detail_url_user2, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Verifica que la tarea de User2 no cambió
        self.assertEqual(
            Task.objects.get(pk=self.task_user2.pk).title, "Tarea de User2"
        )

    # --- PRUEBAS DE ELIMINACIÓN (DELETE) ---

    def test_delete_task_success(self):
        """Asegura que User1 puede eliminar su tarea."""
        self.client.login(username="user1", password="password123")
        response = self.client.delete(self.detail_url_user1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)  # 3 iniciales - 1 eliminada

    def test_delete_task_of_other_user_denied(self):
        """Asegura que User1 NO puede eliminar la tarea de User2."""
        self.client.login(username="user1", password="password123")
        response = self.client.delete(self.detail_url_user2)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.count(), 3)  # La tarea de User2 sigue existiendo

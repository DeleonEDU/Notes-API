from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth import get_user_model

from .models import Note


User = get_user_model()


class NoteTestCase(APITestCase):
    """API tests for Note CRUD operations and access control."""

    def setUp(self):
        """Set up test data and authenticate default user.

        Creates:
        - two users (owner and intruder)
        - one note owned by the authenticated user
        - one note owned by another user
        """
        self.user = User.objects.create_user(
            username="TestUser",
            password="testpassword1245",
        )

        self.other_user = User.objects.create_user(
            username="intruder",
            password="password123",
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.note = Note.objects.create(
            owner=self.user,
            title="TestNote",
            content="Test content to test note",
        )

        self.foreign_note = Note.objects.create(
            owner=self.other_user,
            title="Foreign note",
            content="You should not see this",
        )

    def test_get_notes_list(self):
        """Ensure user receives only their own notes in list view."""
        url = "/api/notes/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_get_note_details(self):
        """Ensure user can retrieve details of their own note."""
        url = f"/api/notes/{self.note.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "TestNote")
        self.assertEqual(response.data["content"], "Test content to note")
        self.assertEqual(response.data["owner"], self.user.id)

    def test_update_note(self):
        """Ensure user can fully update their own note using PUT."""
        url = f"/api/notes/{self.note.id}"

        data = {
            "title": "Updated note",
            "content": "Updated content",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated note")

    def test_partial_update_note(self):
        """Ensure user can partially update their own note using PATCH."""
        url = f"/api/notes/{self.note.id}"

        data = {
            "title": "Partial update note",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Partial update note")

    def test_user_cannot_access_note_of_another_user(self):
        """Ensure user cannot access notes owned by another user.

        Expected behavior:
        - API returns 404 Not Found
        - foreign note is not exposed to unauthorized user
        """
        self.client.force_authenticate(user=self.other_user)

        url = f"/api/notes/{self.note.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from classes.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testuser@mail.ru")
        self.course = Course.objects.create(title="TestCourse", description="TestDescription", owner=self.user)
        self.lesson = Lesson.objects.create(title="TestLesson", description="TestDescription", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("classes:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.lesson.title)

    def test_lesson_create(self):
        url = reverse("classes:lessons_create")
        data = {
            "title": "Test1Lesson",
            "description": "Test1Description",
            "course": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("classes:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "AnotherLesson"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "AnotherLesson")

    def test_lesson_destroy(self):
        url = reverse("classes:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("classes:lessons_list")
        response = self.client.get(url)
        print(response.json())
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    class SubscriptionTestCase(APITestCase):
        def setUp(self):
            self.user = User.objects.create(email="subtest@mail.ru")
            self.course = Course.objects.create(title="Подписка", description="Тест подписки", owner=self.user)
            self.client.force_authenticate(user=self.user)

        def test_subscribe(self):
            url = reverse("users:subscriptions_create")
            data = {"course": self.course.pk}
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data, {"message": 'подписка на курс добавлена'})

        def test_unsubscribe(self):
            url = reverse("users:subscriptions_create")
            data = {"course": self.course.pk}
            Subscription.objects.create(course=self.course, user=self.user)
            response = self.client.post(url, data)
            data = response.json()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(data, {'message': 'подписка удалена'})

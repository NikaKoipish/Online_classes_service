from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from classes.models import Course, Lesson
from classes.validators import VideoSourseValidator
from users.models import Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoSourseValidator(field="video")]


class CourseDetailSerializer(serializers.ModelSerializer):
    count_course_lessons = SerializerMethodField()
    subscription_status = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_course_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_subscription_status(self, obj):
        if Subscription.objects.filter(course=obj):
            return f'Подписка на курс активна'
        return f'Подписка на курс не активирована'

    class Meta:
        model = Course
        fields = "__all__"

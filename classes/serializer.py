from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from classes.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_course_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_course_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ("id", "title", "preview", "description", "count_course_lessons", "lessons")

from rest_framework import serializers


class VideoSourseValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        val = dict(value).get(self.field)
        if "youtube.com" not in val:
            raise serializers.ValidationError(f"{self.field} должен ссылаться только на видео с youtube.com")
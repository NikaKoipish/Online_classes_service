from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from classes.models import Course
from users.models import User, Payment, Subscription
from users.serializer import UserSerializer, PaymentSerializer, UserDetailSerializer, SubscriptionSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    ordering_fields = ('date_of_payment',)
    filterset_fields = ('course', 'lesson', 'payment_method',)
    search_fields = ("payment_method",)


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.get(course=course_item, user=user)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            sub = Subscription.objects.get(user=user, course=course_item).delete()
            message = 'подписка на курс {course.title} удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            sub = Subscription.objects.create(user=user, course=course_item)
            message = 'подписка на курс {course.title} добавлена'
            sub.save()
        # Возвращаем ответ в API
        return Response({"message": message})

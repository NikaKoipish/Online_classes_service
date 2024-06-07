from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView

from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ('date_of_payment',)
    filterset_fields = ('course', 'lesson', 'payment_method',)

from rest_framework.serializers import ModelSerializer

from users.models import User, Payment, Subscription


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "phone", "password")


class UserDetailSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "payment")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "user", "course")

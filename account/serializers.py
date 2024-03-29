from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from wallet.serializers import WalletSerializer

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):

    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "wallet",
            "password"
        ]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["id"].read_only = True
        self.fields["password"].write_only = True

    def create(self, validated_data):

        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):

        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)

        instance.save()

        return instance


class LoginSerilizer(serializers.Serializer):

    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)

    def validate(self, attrs):

        user = authenticate(
            username=attrs["username"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("invalid Credentials")

        attrs["user"] = user

        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, max_length=100)
    new_password = serializers.CharField(required=True, max_length=100)

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Wrong Password")

        if attrs["new_password"] == attrs["old_password"]:
            raise serializers.ValidationError(
                "Old and New Password cannot be the same")

        return attrs

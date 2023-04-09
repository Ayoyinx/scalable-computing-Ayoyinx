from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            "id",
            "amount",
            "book_balance"
        ]


class FundWalletSerializer(serializers.ModelSerializer):

    amount = serializers.FloatField(
        min_value=100.0, max_value=99999.99, required=True)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "amount",
            "book_balance"
        ]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["id"].read_only = True
        self.fields["book_balance"].read_only = True

    def update(self, instance, validated_data):
        instance.amount += validated_data["amount"]
        instance.book_balance += validated_data["amount"]
        instance.save()

        return instance


class TransferWalledSerializer(serializers.Serializer):

    reciever = serializers.PrimaryKeyRelatedField(
        queryset=Wallet.objects.all(), required=True)
    amount = serializers.FloatField(
        min_value=100.0, max_value=45000.0, required=True)

    def validate(self, attrs):

        wallet = self.context["request"].user.wallet
        request = self.context["request"]
        if wallet.amount < attrs["amount"]+100:
            raise serializers.ValidationError("Invalid amount in wallet")

        if wallet.id == attrs["reciever"].id:
            raise serializers.ValidationError("Cannot Transfer to yourself")

        wallet = request.user.wallet
        wallet.amount -= attrs["amount"]
        wallet.save()

        reciever = attrs["reciever"]
        reciever.amount += attrs["amount"]
        reciever.save()

        return attrs

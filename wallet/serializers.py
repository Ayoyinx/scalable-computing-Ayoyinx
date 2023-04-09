from rest_framework import serializers

from .models import Wallet, History


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = [
            "id",
            "amount",
        ]


class FundWalletSerializer(serializers.ModelSerializer):

    amount = serializers.FloatField(
        min_value=100.0, max_value=99999.99, required=True)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "amount",
        ]

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        self.fields["id"].read_only = True

    def update(self, instance, validated_data):
        request = self.context["request"]
        instance.amount += validated_data["amount"]
        instance.save()

        reciever = request.user.wallet
        History.objects.create(
            user=request.user,
            reciever=reciever,
            name=reciever.user.username,
            action="fund",
            amount=validated_data["amount"]
        )

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
            raise serializers.ValidationError(
                {"amount": "Invalid amount in wallet"})

        if wallet.id == attrs["reciever"].id:
            raise serializers.ValidationError(
                {"amount": "Cannot Transfer to yourself"})

        wallet = request.user.wallet
        wallet.amount -= attrs["amount"]
        wallet.save()

        reciever = attrs["reciever"]
        reciever.amount += attrs["amount"]
        reciever.save()

        History.objects.create(
            user=request.user,
            reciever=reciever,
            name=reciever.user.username,
            action="transfer",
            amount=attrs["amount"]
        )

        return attrs


class HistorySerilizer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ["name", "amount", "action", "date"]

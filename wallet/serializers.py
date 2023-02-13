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
    
    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.fields["id"].read_only = True
        self.fields["amount"].read_only = True
        self.fields["book_balance"].read_only = True
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import History
from .serializers import FundWalletSerializer, WalletSerializer, TransferWalledSerializer


class FundWalletView(generics.UpdateAPIView):
    serializer_class = FundWalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


class TransferFundView(generics.GenericAPIView):
    serializer_class = TransferWalledSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Transferred Successfully"}, status=status.HTTP_200_OK)


class RetrieveWalletView(generics.RetrieveAPIView):

    serializer_class = WalletSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

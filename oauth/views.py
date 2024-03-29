import requests

from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope

from .forms import LoginForm
from wallet.serializers import TransferWalletSerializer
from . import serializers


User = get_user_model()


class UserInfoView(generics.RetrieveAPIView):

    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAuthenticated, TokenHasScope]
    authentication_classes = [OAuth2Authentication]
    required_scopes = ["read"]

    def get_object(self):
        return self.request.user


class LoginOauthView(generic.FormView):

    template_name = "login.html"
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

    def get_success_url(self):

        return self.request.GET["next"]


class TransferAmountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ["transfer"]
    serializer_class = TransferWalletSerializer
    authentication_classes = [OAuth2Authentication]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"status": "success", "message": "Transfer Successful"}, status=status.HTTP_200_OK)


class BookStoreAuthView(generics.GenericAPIView):
    serializer_class = serializers.BookStoreAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        token_response = serializer.validated_data["token_res"]
        token_data = token_response.json()
        access_token = token_data['access_token']

        user_response = requests.get(
            f'http://booksoreapi-env.eba-3igtf73b.us-east-1.elasticbeanstalk.com/oauth/userinfo/',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )

        if user_response.status_code != 200:
            # Return an error response if user info retrieval fails
            return Response({'error': 'Failed to retrieve user info from Bookstore'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_response.json()
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        # Create a new user account with the user info
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(None)
            )
        except:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Failed to authenticate user from BookStore'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token)
        }

        return Response(response, status=status.HTTP_200_OK)


class GoogleAuthView(generics.GenericAPIView):

    serializer_class = serializers.GoogleAuthSerializer

    def post(self, request):

        # Exchange the authorization code for an access token and user info
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        token_response = serializer.validated_data["token_res"]
        token_data = token_response.json()
        access_token = token_data['access_token']

        user_response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}')

        if user_response.status_code != 200:
            # Return an error response if user info retrieval fails
            return Response({'error': 'Failed to retrieve user info from Google'}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_response.json()
        email = user_data.get('email')
        first_name = user_data.get('given_name')
        last_name = user_data.get('family_name')

        # Create a new user account with the user info
        try:
            user = User.objects.create(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(None)
            )
        except:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Failed to authenticate user from Google'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token)
        }

        return Response(response, status=status.HTTP_200_OK)


class UploadTransactionAuthView(generics.GenericAPIView):

    serializer_class = serializers.UploadTransactionAuthSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_response = serializer.validated_data["token_res"]

        token_data = token_response.json()
        access_token = token_data['access_token']
        history = serializer.validated_data["history"]
        amount = history.amount

        if history.action == "transfer":
            amount = 0 - amount

        response = requests.post(
            "http://fianancetracker-env.eba-zzxqpwbf.us-east-1.elasticbeanstalk.com/oauth/add-transaction/",
            headers={"Authorization": f"Bearer {access_token}"},

            json={
                "amount": amount,
                "category": "wallet",
                "date": str(history.date)
            }
        )

        if response.status_code != 201:
            return Response({"status": "failed", "message": f"Unable to Perform Transaction"}, status=status.HTTP_400_BAD_REQUEST)

        history.uploaded = True
        history.save()

        return Response({"status": "status", "message": "Transaction Added"})

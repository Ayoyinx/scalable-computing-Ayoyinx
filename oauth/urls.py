from django.urls import path

from oauth2_provider.views import AuthorizationView, TokenView

from . import views

urlpatterns = [
    path("authorize/", AuthorizationView.as_view(), name="oauth-authoize"),
    path("token/", TokenView.as_view(), name="oauth-login"),
    path("login/", views.LoginOauthView.as_view(), name="oauth-login"),
    path("waller-auth/", views.FinanceTrackerAuthView.as_view(), name="wallet-auth"),
    path("google-auth/", views.GoogleAuthView.as_view(), name="google-auth")
]

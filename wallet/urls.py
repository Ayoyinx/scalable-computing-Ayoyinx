from django.urls import path
from . import views

urlpatterns = [
    path("", views.RetrieveWalletView.as_view(), name="fetch"),
    path("transfer/", views.TransferFundView.as_view(), name="transfer"),
    path("fund/", views.FundWalletView.as_view(), name="fund")
]
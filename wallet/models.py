from random import randint
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Wallet(models.Model):

    def generate_id(self):

        return randint(int('1'*15), int('9'*15))

    id = models.PositiveBigIntegerField(
        primary_key=True,
        unique=True,
        null=False,
        blank=False
    )

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="wallet"
    )

    amount = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0)
        ]
    )

    book_balance = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0)
        ]
    )

    def __str__(self):
        return f"{self.user} {self.id}"

    def save(self, *args, **kwargs):

        if not self.id:
            self.id = self.generate_id()
        self.full_clean()

        return super().save(*args, **kwargs)


class History(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    reciever = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
    amount = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0)
        ]
    )

    def __str__(self) -> str:
        return f'{self.user} {self.name}'

from random import randint
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()
class Wallet(models.Model):

    def generate_id(self):
        id = randint(11111111111, 99999999999)

        while(Wallet.objects.filter(id=id).exists()):
            id = randint(11111111111, 99999999999)
        
        return id

    id = models.PositiveIntegerField(
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
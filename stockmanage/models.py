from django.db import models
from django.utils import timezone

# Create your models here.


class stockmanage(models.Model):
    symbol = models.CharField(max_length=10)
    sharePriceBought = models.DecimalField(max_digits=6, decimal_places=2)
    numberOfShares = models.DecimalField(max_digits=6, decimal_places=2)
    dividendAmount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    dividendPercentage = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
    shareBoughtDate = models.DateField(default=timezone.now)

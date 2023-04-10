from django.db import models
from django.utils import timezone


class indexetfmanage(models.Model):
    indexName = models.CharField(max_length=10)
    fundType = models.CharField(max_length=10)

    def __str__(self):
        return self.indexName

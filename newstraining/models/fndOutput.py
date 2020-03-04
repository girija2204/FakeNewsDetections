from django.db import models
from newstraining.models.fndModel import FNDModel


class FNDOutput(models.Model):
    variableName = models.CharField(null=False, max_length=100)
    variableSymbol = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f"Name: {self.variableName}, Type: {self.variableSymbol}"

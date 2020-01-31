from django.db import models
from newstraining.models.fndModel import FNDModel


class FNDInput(models.Model):
    variableName = models.CharField(null=False, max_length=100)
    variableSymbol = models.CharField(null=False, max_length=100)
    fndModel = models.ForeignKey(FNDModel, on_delete=models.CASCADE)
    trainingIndicator = models.CharField(null=False, max_length=1)

    def __str__(self):
        return f"Name: {self.variableName}, Type: {self.variableSymbol}"

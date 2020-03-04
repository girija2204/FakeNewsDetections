from django.db import models


class FNDInput(models.Model):
    variableName = models.CharField(null=False, max_length=100)
    variableSymbol = models.CharField(null=False, max_length=100)
    trainingIndicator = models.CharField(null=False, max_length=1)

    def __str__(self):
        return f"Name: {self.variableName}, Type: {self.variableSymbol}"

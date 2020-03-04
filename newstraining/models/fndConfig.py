from django.db import models
from newstraining.models.fndModel import FNDModel


class FNDConfig(models.Model):
    name = models.CharField(null=False, max_length=100)
    fndType = models.CharField(null=False, max_length=100)
    fndModel = models.ForeignKey(FNDModel, on_delete=models.CASCADE)
    fndInputs = models.CharField(null=False,max_length=100)
    fndOutput = models.CharField(null=True,max_length=100)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.fndType}"

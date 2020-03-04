from django.db import models

# from .fndConfig import FNDConfig


class FNDModel(models.Model):
    name = models.CharField(null=False, max_length=100)
    algorithm = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.algorithm}"

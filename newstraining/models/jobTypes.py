from django.db import models

class JobTypes(models.Model):
    typeName = models.CharField(null=False,max_length=100)
    code = models.CharField(null=False,max_length=100)
    expression = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f"Job Type: {self.typeName}, Job Code: {self.code}, Job Expression: {self.expression}"
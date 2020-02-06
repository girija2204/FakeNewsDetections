from django.db import models
from newstraining.models.fndConfig import FNDConfig


class FNDRunDetail(models.Model):
    runStartTime = models.DateTimeField(null=False)
    runEndTime = models.DateTimeField(null=False)
    historyStartTime = models.DateTimeField()
    historyEndTime = models.DateTimeField()
    fndConfig = models.ForeignKey(FNDConfig, on_delete=models.CASCADE)

    def __str__(self):
        return f"Run start time: {self.runStartTime}, Run end time: {self.runEndTime}, History start time: {self.historyStartTime}, History end time: {self.historyEndTime}"

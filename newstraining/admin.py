from django.contrib import admin
from newstraining.models import (
    fndConfig,
    fndInput,
    fndModelAttribute,
    fndModel,
    fndOutput,
    fndRunDetail,
    jobTypes
)

fndModels = [
    fndConfig.FNDConfig,
    fndOutput.FNDOutput,
    fndModel.FNDModel,
    fndModelAttribute.FNDModelAttribute,
    fndInput.FNDInput,
    fndRunDetail.FNDRunDetail,
    jobTypes.JobTypes,
]
admin.site.register(fndModels)

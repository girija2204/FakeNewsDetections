from django.contrib import admin
from newstraining.models import (
    fndConfig,
    fndInput,
    fndModelAttribute,
    fndModel,
    fndOutput,
    fndRunDetail,
)

fndModels = [
    fndConfig.FNDConfig,
    fndOutput.FNDOutput,
    fndModel.FNDModel,
    fndModelAttribute.FNDModelAttribute,
    fndInput.FNDInput,
    fndRunDetail.FNDRunDetail,
]
admin.site.register(fndModels)

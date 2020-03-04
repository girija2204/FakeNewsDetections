from django import forms
from django.urls import reverse
from newsextractor.models import NewsArticle
from newstraining.models.fndOutput import FNDOutput
from newstraining.models.fndModel import FNDModel
from newstraining.models.fndInput import FNDInput
from newstraining.models.jobTypes import JobTypes
from django.conf import settings

log = settings.LOG


class NewsPredictionForm(forms.Form):
    date_posted = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    title = forms.CharField(max_length=1000)
    content = forms.CharField(widget=forms.Textarea)
    author = forms.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse("prediction-detail")


class NewsTrainingForm(forms.Form):
    job_types = forms.ModelChoiceField(queryset=JobTypes.objects.values_list('typeName', flat=True).distinct())
    job_codes = forms.ModelChoiceField(queryset=JobTypes.objects.values_list('code', flat=True))
    input_types = forms.ModelMultipleChoiceField(queryset=FNDInput.objects.values_list('variableName', flat=True),
                                                 widget=forms.CheckboxSelectMultiple)
    output_types = forms.ModelMultipleChoiceField(queryset=FNDOutput.objects.values_list('variableName', flat=True),
                                                  widget=forms.CheckboxSelectMultiple)
    algorithm_types = forms.ModelChoiceField(queryset=FNDModel.objects.values_list('algorithm', flat=True))
    # job_codes = forms.ModelChoiceField(queryset=JobTypes.objects.none())

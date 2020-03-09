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
    minutes_choices = (
        ("--", "--"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("5", "5"),
        ("10", "10"),
        ("15", "15"),
        ("30", "30"),
        ("45", "45")
    )
    minutes_field = forms.CharField(label='',widget=forms.Select(choices=minutes_choices,attrs={'class':'minutes_choices'}),initial='--')
    hour_choices = (
        ("--", "--"),
        ("1","1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("6", "6"),
        ("12", "12")
    )
    hour_field = forms.CharField(widget=forms.Select(choices=hour_choices,attrs={'class':'hour_choices'}),label='',initial='--')
    hour_start_choices = (
        ("--", "--"),
        ("0", "0"),
        ("1","1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
        ("21", "21"),
        ("22", "22"),
        ("23", "23")
    )
    daily_hour_start_field = forms.CharField(widget=forms.Select(choices=hour_start_choices,attrs={'class':'hour_start_choices'}),label='',initial='--')
    minute_start_choices = (
        ("--", "--"),
        ("00", "00"),
        ("15", "15"),
        ("30", "30"),
        ("45", "45")
    )
    daily_minute_start_field = forms.CharField(widget=forms.Select(choices=minute_start_choices,attrs={'class':'minute_start_choices'}),label='',initial='--')
    job_types = forms.ModelChoiceField(queryset=JobTypes.objects.values_list('typeName', flat=True).distinct(),
                                       label='', widget=forms.Select)
    input_types = forms.ModelMultipleChoiceField(queryset=FNDInput.objects.values_list('variableName', flat=True),
                                                 widget=forms.CheckboxSelectMultiple,
                                                 label='')
    output_types = forms.ModelMultipleChoiceField(queryset=FNDOutput.objects.values_list('variableName', flat=True),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  label='')
    algorithm_types = forms.ModelChoiceField(queryset=FNDModel.objects.values_list('algorithm', flat=True), label='',
                                             widget=forms.Select)
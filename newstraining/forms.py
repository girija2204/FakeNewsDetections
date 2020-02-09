from django import forms
from newsextractor.models import NewsArticle


class NewsArticlePredictionForm(forms.ModelForm):
    date_posted = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))

    class Meta:
        model = NewsArticle
        fields = ["title", "content", "author", "date_posted"]

from django import forms
from django.urls import reverse
from newsextractor.models import NewsArticle


class NewsArticlePredictionForm(forms.Form):
    date_posted = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    title = forms.CharField(max_length=1000)
    content = forms.CharField(widget=forms.Textarea)
    author = forms.CharField(max_length=1000)

    def get_absolute_url(self):
        # return reverse('prediction-detail', kwargs={'pk': self.pk})
        return reverse("prediction-detail")

    # class Meta:
    #     model = NewsArticle
    #     fields = ["title", "content", "author", "date_posted"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

from newsextractor.models import NewsArticle
from newstraining.fndDriver import FNDDriver
from .forms import NewsArticlePredictionForm
from django.views.generic import FormView, DetailView, TemplateView
from newstraining.fndContext import FNDContext
from newstraining.algorithm.algorithmAdapter import AlgorithmAdapter
import pandas as pd
import pdb

log = settings.LOG


def train(request):
    log.debug("Inside view for training")
    fndDriver = FNDDriver()
    fndDriver.run()
    context = {"news_articles": "hello modekl", "title": "Portal - Homepage"}
    return render(request, "newsextractor/home.html", context)


class NewsArticlePredictionFormView(FormView):
    form_class = NewsArticlePredictionForm
    template_name = "newstraining/prediction-form.html"
    success_url = "newstraining/prediction-detail.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            fndContext = FNDContext(processName="prediction")
            algoAdapter = AlgorithmAdapter()
            formdata = pd.DataFrame.from_records(
                [
                    {
                        "content": form.cleaned_data["content"],
                        "author": form.cleaned_data["author"],
                    }
                ]
            )
            classPredicted = algoAdapter.initiatePrediction(
                predictionInput=formdata, fndContext=fndContext
            )
            log.debug(f"Predicted class is: {classPredicted}")
            context = {
                "content": form.cleaned_data["content"],
                "classPredicted": classPredicted,
                "title": form.cleaned_data["title"],
                "author": form.cleaned_data["author"],
                "date_posted": form.cleaned_data["date_posted"],
            }
            return render(request, self.success_url, context=context)

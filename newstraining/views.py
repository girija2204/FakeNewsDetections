from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.conf import settings

from newsextractor.models import NewsArticle
from newstraining.fndDriver import FNDDriver
from .forms import NewsArticlePredictionForm
from django.views.generic import FormView
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


def predict(request):
    log.debug("Inside view for prediction")
    if request.method == "POST":
        log.debug("hello there, doing prediction")
    else:
        fndDriver = FNDDriver()
        fndDriver.run()
    context = {"news_articles": "hello modekl", "title": "Portal - Homepage"}
    return render(request, "newsextractor/home.html", context)


class NewsArticlePredictionView(LoginRequiredMixin, FormView):
    form_class = NewsArticlePredictionForm
    template_name = "newstraining/prediction-form.html"
    success_url = "newstraining/home.html"

    def form_valid(self, form):
        fndContext = FNDContext(processName="prediction")
        algoAdapter = AlgorithmAdapter()
        # pdb.set_trace()
        # formdata = pd.Series({'author': form.cleaned_data['author'],'content': form.cleaned_data['content']}).to_frame()
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
        return super().form_valid(form)


if __name__ == "__main__":
    train()

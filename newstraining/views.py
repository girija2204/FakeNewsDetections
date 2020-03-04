from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

from newsextractor.models import NewsArticle
from newstraining.fndDriver import FNDDriver
from newstraining.models.fndModel import FNDModel
from newstraining.models.jobTypes import JobTypes
from .forms import NewsPredictionForm, NewsTrainingForm
from django.views.generic import FormView, DetailView, TemplateView, View
from newstraining.fndContext import FNDContext
from newstraining.algorithm.algorithmAdapter import AlgorithmAdapter
from newstraining.trainingEnums import TrainingEnums
import pandas as pd
import threading
from .jobs import DailyTrainingJobs, ManualTrainingJobs
import pdb

log = settings.LOG


def train(request):
    log.debug("Inside view for training")
    fndDriver = FNDDriver()
    fndDriver.run()
    context = {"news_articles": "hello modekl", "title": "Portal - Homepage"}
    return render(request, "newsextractor/home.html", context)


def load_job_codes(request):
    print(request)
    jobType = request.GET.get('job_types')
    print(f'job type: {jobType}')
    jobCode = JobTypes.objects.filter(typeName=jobType).first()
    return render(request, 'newstraining/training_job_codes.html', {'jobCode': jobCode})


def threadRun(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType):
    log.debug(f'Inside thread run')
    fndDriver = FNDDriver()
    fndDriver.run(selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType)


class NewsArticleTrainingFormView(LoginRequiredMixin, FormView):
    form_class = NewsTrainingForm
    template_name = "newstraining/training-form.html"
    success_url = "newstraining/training-detail.html"

    def post(self, request, *args, **kwargs):
        selectedJobCode = request.POST.get('job_codes')
        selectedInputTypes = request.POST.getlist('input_types')
        selectedOutputType = request.POST.get('output_types')
        selectedAlgorithmType = request.POST.get('algorithm_types')
        selectedJobType = request.POST.get('job_types')
        log.debug("Inside view for training")
        log.debug(f'selected input types:{selectedOutputType}')
        fndDriver = FNDDriver()
        configuration = fndDriver.saveConfiguration(selectedJobType,selectedAlgorithmType,selectedInputTypes,selectedOutputType)
        if configuration.fndType.lower() == TrainingEnums.DAILY_TRAINING.value.lower():
            dnt = DailyTrainingJobs()
            t = threading.Thread(target=dnt.run,
                                 args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType])
            t.start()
        elif configuration.fndType.lower() == TrainingEnums.MANUAL_TRAINING.value.lower():
            mnt = ManualTrainingJobs()
            t = threading.Thread(target=mnt.run,
                                 args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType])
            t.start()
        context = {"news_articles": "hello modekl", "title": "Portal - Homepage"}
        return render(request, self.success_url, context=context)


class NewsArticlePredictionFormView(LoginRequiredMixin, FormView):
    form_class = NewsPredictionForm
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

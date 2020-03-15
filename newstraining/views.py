from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings

from newsextractor.models import NewsArticle
from newstraining.fndDriver import FNDDriver
from newstraining.models.fndInput import FNDInput
from newstraining.models.fndOutput import FNDOutput
from newstraining.models.fndModel import FNDModel
from newstraining.models.jobTypes import JobTypes
from newstraining.models.fndRunDetail import FNDRunDetail
from .forms import NewsPredictionForm, NewsTrainingForm
from django.views.generic import FormView, DetailView, TemplateView, View, ListView
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
    # template_name = "newstraining/training-detail.html"
    success_url = "newstraining/training-detail.html"

    def post(self, request, *args, **kwargs):
        log.debug("Inside view for training")
        selectedInputTypes = request.POST.getlist('input_types')
        selectedOutputType = request.POST.get('output_types')
        selectedAlgorithmType = request.POST.get('algorithm_types')
        selectedJobType = request.POST.get('job_types')
        fndDriver = FNDDriver()
        configuration = fndDriver.saveConfiguration(selectedJobType, selectedAlgorithmType, selectedInputTypes,
                                                    selectedOutputType)
        selectedMin = None
        selectedHour = None
        selectedDailyHourField = None
        selectedDailyMinField = None
        if selectedJobType == TrainingEnums.DAILY_TRAINING.value:
            log.debug(f'Selected Job Type: {selectedJobType}')
            if request.POST.get('minutes_field') != '--':
                selectedMin = request.POST.get('minutes_field')
                log.debug(f'Selected Minutes: {selectedMin}')

            elif request.POST.get('hour_field') != '--':
                selectedHour = request.POST.get('hour_field')
                log.debug(f'Selected Hours: {selectedHour}')

            elif request.POST.get('daily_hour_start_field') != '--':
                selectedDailyHourField = request.POST.get('daily_hour_start_field')
                selectedDailyMinField = request.POST.get('daily_minute_start_field')
                log.debug(f'selected Daily Hour field: {selectedDailyHourField}')
                log.debug(f'selected Daily Minute field: {selectedDailyMinField}')

            dnt = DailyTrainingJobs()
            t = threading.Thread(target=dnt.run,
                                 args=[selectedJobType, selectedAlgorithmType, selectedInputTypes,
                                       selectedOutputType, selectedMin, selectedHour, selectedDailyHourField,
                                       selectedDailyMinField])
            t.start()

        elif configuration.fndType.lower() == TrainingEnums.MANUAL_TRAINING.value.lower():
            mnt = ManualTrainingJobs()
            t = threading.Thread(target=mnt.run,
                                 args=[selectedJobType, selectedAlgorithmType, selectedInputTypes, selectedOutputType])
            t.start()
        inputs = []
        output = None
        for input in configuration.fndInputs:
            inputs.append(FNDInput.objects.filter(id=input).values_list('variableName', flat=True).first())
        output = FNDOutput.objects.filter(id=configuration.fndOutput).values_list('variableName', flat=True).first()
        context = {"inputs": inputs, "output": output, "algorithm": configuration.fndModel.name}
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


class RunDetailsListView(LoginRequiredMixin, ListView):
    model = FNDRunDetail
    template_name = "newstraining/recent_run_details.html"
    context_object_name = "run_details"
    # ordering = ["-date_posted"]

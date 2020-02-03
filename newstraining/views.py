from django.shortcuts import render
from django.conf import settings
from newstraining.ntDriver import FNDDriver

log = settings.LOG


def train(request):
    log.debug("Inside view for training")
    # if request.method == "POST":
    fndDriver = FNDDriver()
    fndDriver.run()
    context = {"news_articles": "hello modekl", "title": "Portal - Homepage"}
    return render(request, "newsextractor/home.html", context)


if __name__ == "__main__":
    train()

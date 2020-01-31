from django.shortcuts import render
from django.conf import settings
from newstraining.ntDriver import FNDDriver

log = settings.LOG


def train(request):
    log.debug("Inside view for training")
    # if request.method == "POST":
    fndDriver = FNDDriver()
    fndDriver.run()
    return "training done"


if __name__ == "__main__":
    train()

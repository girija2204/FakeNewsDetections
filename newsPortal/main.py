from django.conf import settings
from newsPortal.newsPortal.newstraining.ntDriver import FNDDriver

log = settings.LOG


def main():
    log.debug("hello logger")
    fndDriver = FNDDriver()
    fndDriver.run()


if __name__ == "__main__":
    main()

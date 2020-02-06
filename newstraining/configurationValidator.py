import os


class ConfigurationValidator:
    @staticmethod
    def isNotNull(configurationObject):
        if configurationObject is None:
            print(f"configuration error for: {str(configurationObject)}")

    @staticmethod
    def isDirectory(path):
        if not os.path.isdir(path):
            print(f"the provided path does not exist: {path}")
            return

        if not os.access(path, os.R_OK | os.W_OK):
            print(f"the provided path has no read and write permissions")
            return

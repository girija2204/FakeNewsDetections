import os
import pdb


class ConfigurationValidator:
    @staticmethod
    def isNotNull(key, configurationObject):
        if configurationObject is None:
            print(f"configuration error for: {key}")

    @staticmethod
    def isDirectory(key, path):
        if not os.path.isdir(path):
            print(f"the provided path does not exist: {key}")
            return

        if not os.access(path, os.R_OK | os.W_OK):
            print(f"the provided path has no read and write permissions: {key}")
            return

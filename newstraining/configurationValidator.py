import os
import pdb
from newstraining.exceptions.configurationException import ConfigurationException
from newstraining.exceptions.invalidPathException import InvalidPathException


class ConfigurationValidator:
    @staticmethod
    def isNotNull(key, configurationObject):
        if configurationObject is None:
            raise ConfigurationException(f"configuration error for: {key}")

    @staticmethod
    def isDirectory(key, path):
        if not os.path.isdir(path):
            raise InvalidPathException(f"the path provided does not exist: {key}")

        if not os.access(path, os.R_OK | os.W_OK):
            raise PermissionError(
                f"the provided path has no read and write permissions: {key}"
            )

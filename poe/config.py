import logging
import os


settings = {}

settings["BASE_PATH"] = os.path.dirname(os.path.realpath(__file__))
execfile(os.path.join(settings["BASE_PATH"], "settings.py"), settings)

# override default settings
try:
    local_settings = {}
    execfile(os.path.join(settings["BASE_PATH"], "local_settings.py"),
             local_settings)

    for key, value in local_settings.iteritems():
        settings[key] = value
except IOError:
    pass

settings["DB_PATH"] = os.path.join(settings["BASE_PATH"],
                                   settings["DB_FILENAME"])

logging.basicConfig(level=settings["LOGGING_LEVEL"])
logging.getLogger("sqlalchemy.engine").setLevel(settings["LOGGING_LEVEL"])

import logging


settings = {}
execfile("settings.py", settings)

# override default settings
try:
    local_settings = {}
    execfile("local_settings.py", local_settings)

    for key, value in local_settings.iteritems():
        settings[key] = value
except IOError:
    pass


logging.basicConfig(level=settings["LOGGING_LEVEL"])

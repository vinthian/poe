Path of Exile API
=================
*Python API to consume resources from official Path of Exile web site*

web_api
-------
*under construction*

local settings
--------------
Create a file called "local_settings.py" in the "poe" module. This file should not be committed and  is currently in .gitignore:


**poe/local_settings.py**
```python
import logging


LOGGING_LEVEL = logging.DEBUG

USERNAME = "youremail@pathofexile.com"
PASSWORD = "p4ssw0rd"
```
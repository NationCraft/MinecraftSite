#!/usr/bin/python3
activate_this = '/var/www/minecraft_site/minecraft_site/venv/bin/activate$
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/minecraft_site/")

from minecraft_site.site import app as application
application.secret_key = 'enter_secret_key'


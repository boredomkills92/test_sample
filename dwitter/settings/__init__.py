
import os

environment = os.environ.get('environment')

if environment.upper() == "prod".upper():
	print("Production settings are loaded")
	from .prod import *
else:
	print("Warning! Dev settings are loaded")
	from .dev import *
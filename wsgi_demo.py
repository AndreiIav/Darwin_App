import os

from application import init_app

os.environ["CONFIG_TYPE"] = "config.DemoConfig"
app = init_app()

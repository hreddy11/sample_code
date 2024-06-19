from airflow.plugins_manager import AirflowPlugin
from my_plugin.views import MyPluginView

class MyCustomPlugin(AirflowPlugin):
    name = "my_custom_plugin"
    flask_blueprints = [MyPluginView]

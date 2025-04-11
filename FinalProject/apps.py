from django.apps import AppConfig

# Define a configuration class for the FinalProject app

class FinalProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'FinalProject'       # Specify the name of the app (must match the app directory name)

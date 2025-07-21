from django.apps import AppConfig


class AnalysecompteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analyseCompte'

    def ready(self):
        from . import main as m
        print("initalisation")
        m.initialisation()
        print("initialisation réussie")
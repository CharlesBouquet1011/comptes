from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("upload/",include(views.upload)), #puis mettre view.fonction avec fonction dans le fichier views
    path("annee/",include(views.analyseAnnee)),
    path("mois/",include(views.analyseMois)),
    path("filtrer/",include(views.filtre)),

    path("calcImpots/",include(views.calcImpots)),

    path("calcTotal",include(views.somme)) #à compléter

    
]
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("upload/",views.upload), #puis mettre view.fonction avec fonction dans le fichier views
    path("annee/",views.analyseAnnee),
    path("mois/",views.analyseMois),
    path("filtrer/",views.filtre),

    path("calcImpots/",views.calcImpots),

    path("calcTotal",views.somme) #à compléter

    
]
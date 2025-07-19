from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("upload/",views.upload), #puis mettre view.fonction avec fonction dans le fichier views, fait
    path("annee/",views.analyseAnnee), #fait
    path("mois/",views.analyseMois),
    path("verify/",views.verify),
    path("filtrer/",views.filtre),

    path("calcImpots/",views.calcImpots),

    path("calcTotal",views.somme) #à compléter

    
]
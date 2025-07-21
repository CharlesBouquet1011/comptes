from django.contrib import admin
from django.urls import path,include
from . import views

##IL FAUDRAIT AJOUTER LE SUPPORT DE PLUSIEURS COMPTES BANCAIRES (là tout est le même) (aller dans des fichiers différents en fonction)
urlpatterns = [
    path("upload/",views.upload), #puis mettre view.fonction avec fonction dans le fichier views, fait
    path("annee/",views.analyseAnnee), #fait
    path("mois/",views.analyseMois), #fait
    path("verify/",views.verify),
    path("filtrer/",views.filtre),
    path("pretraitement/",views.pretraitement),#fait
    path("calcImpots/",views.calcImpots),
    path("camembert/",views.camembert),
    path("calcTotal",views.somme) #à compléter

    
]
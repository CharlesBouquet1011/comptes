from django.shortcuts import render
from django.http import JsonResponse
import json
from . import analyse as a
import pandas as pd
from . import main as m
import os
Domaine="http://localhost:8000/"
def upload(request):
    """
    upload le fichier csv à traiter
    
    """
    try:
        if request.method=="POST":
            file=request.FILES.get("file") #je récupère le file dans le data envoyé dans le body Django met les fichiers tout seul dans request.FILES
            #le frontend DOIT envoyer un objet de type File JS
            #enregistrement et traitement du fichier comme je veux maintenant
            if file and file.name.endswith(".csv"):
                if file.name not in os.listdir("./donnees_a_traiter"):
                    chemin=f"./donnees_a_traiter/{file.name}"
                    with open(chemin,"wb+") as destination:
                        for partie in file.chunks():
                            destination.write(partie)
                    return JsonResponse({"ok":"ok"},status=200)
                else:
                    print("Fichier déjà présent")
                    return JsonResponse({"error":"Le fichier est déjà présent"},status=409)
                
            else:
                return JsonResponse({"error":"Fichier incorrect"},status=406)
            
    except Exception as e:
        print("erreur :", e)
        return JsonResponse({"error": "Erreur serveur"},status=500)
        


def analyseAnnee(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body.decode('utf-8'))
            annee=data.get("annee") 
            nonErr=a.AnalyseAnnee(annee) #ici l'année est un string
            if not nonErr:
                return JsonResponse({"error: une erreur est survenue"},status=500)
            else:
                chem=f"{Domaine}exports/{annee}"
                
                chemins=[f"{chem}/Depenses_{annee}.jpg",f"{chem}/Gains_{annee}.jpg",f"{chem}/Bilan_{annee}.jpg"]
                return JsonResponse({"chemins":chemins,"noms":[f"Depenses {annee}", f"Gains {annee}", f"Bilan {annee}"]},status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=406)
    

def analyseMois(request):
    if request.method=="POST":
        try:
            data=json.load(request.body)
            annee=data.get("annee") 
            mois=data.get("mois")
            nonErr=a.AnalyseMois(annee,mois)
            if not nonErr:
                return JsonResponse({"error: une erreur est survenue"},status=500)
            else:
                chem=f"../exports/{annee}/{mois}_{annee}"
                nom="Mois"
                chemins=[f"{chem}/Depenses_{nom}",f"{chem}/Gains_{nom}",f"{chem}/Bilan_{nom}"]
                return JsonResponse({"chemins":chemins},status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=400)
    pass

def somme(request):
    if request.method=="POST":
        try:
            data=json.load(request.body)
            criteres=data.get("criteres") #critere: {clé:(valeur,strict)} ou la clé est une colonne du DataFrame, valeur est une valeur que ça peut prendre et strict est utile pour les chaines (si strict: == sinon substring)
            colonnes=data.get("colonnes") #colonnes dont on veut obtenir la somme liste [] Chaque colonne doit être dans le DataFrame
            df,doublon=m.importPasse()
            df=a.filtre(df,criteres)
            sortie={colonne: df[colonnes].sum() for colonne in colonnes}
            return JsonResponse(sortie, status=200)


        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=400)
    
def get_columns(request):
    if request.method=="GET":
        try:
            df=m.importPasse()
            data=[col for col in df.columns]
            return JsonResponse({"data":data},status=200)
        except Exception as e:
            print("Une erreur est survenue:",e)
            return JsonResponse({"error":"Erreur serveur"},status=500)
# Create your views here.

def filtre(request): #on affichera le DF en forme de tableau seulement pour les entrées correspondantes au critère
    pass    
def calcImpots(request): #probablement compliqué 
    pass

def verify(request): #vérifie que les données enregistrées correspondent aux données de la banque jusqu'à la date de la dernière donnée enregistrée
    #permet de détecter aisément une incohérence
    pass
from django.shortcuts import render
from django.http import JsonResponse
import json
import analyse as a
import pandas as pd
import main as m
from uploadForm import UploadCSVForm
def upload(request):
    """
    upload le fichier csv à traiter
    
    """
    if request.method=="POST":
        file=request.FILES.get("file") #je récupère le file dans le data envoyé dans le body Django met les fichiers tout seul dans request.FILES
        #le frontend DOIT envoyer un objet de type File JS
        #enregistrement et traitement du fichier comme je veux maintenant

        pass
    pass

def analyseAnnee(request):
    if request.method=="POST":
        try:
            data=json.load(request.body)
            annee=data.get("annee") 
            nonErr=a.AnalyseAnnee(annee) #ici l'année est un string
            if not nonErr:
                return JsonResponse({"error: une erreur est survenue"},status=500)
            else:
                chem=f"../exports{annee}"
                nom="Annee"
                chemins=[f"{chem}/Depenses_{nom}",f"{chem}/Gains_{nom}",f"{chem}/Bilan_{nom}"]
                return JsonResponse({"chemins":chemins},status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=400)
    

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

def get_upload_forms_schema(request):
    if request.method=="GET":
        try:
            form=UploadCSVForm()
            form_dict={"champs:":[
                {
                    'name':name,
                    'label':field.label,
                    'required':field.required,
                    'widget':field.widget,
                    'type':type(field).__name__,

                }

            for name,field in form.fields.items()

            ]} #on n'utilise pas le forms sauf ici, à simplifier donc
            return JsonResponse(form_dict,status=200)
        except Exception as e:
            print("Erreur:",e)
            return JsonResponse({"error":"Erreur serveur"},status=500)

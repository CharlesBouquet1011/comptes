from django.shortcuts import render
from django.http import JsonResponse
import json
from . import analyse as a
import pandas as pd
from . import main as m
import os
Domaine="http://localhost:8000/"
def upload(request): #il faudrait enchaîner sur le traitement des données (les séparer pour les répartir dans les dossiers des mois correspondants)
    #probablement une autre API à faire pour ça
    """
    upload le fichier csv à traiter
    parametre:
        -le fichier à upload
    retour:
        -un statut sur la réussite ou l'échec de l'upload
    
    """
    try:
        if request.method=="POST":
            file=request.FILES.get("file") #je récupère le file dans le data envoyé dans le body Django met les fichiers tout seul dans request.FILES
            #le frontend DOIT envoyer un objet de type File JS
            #enregistrement et traitement du fichier comme je veux maintenant
            if file and file.name.endswith(".csv"):
                
                    chemin="./donnees_a_traiter/a_traiter.csv"
                    with open(chemin,"wb+") as destination:
                        for partie in file.chunks():
                            destination.write(partie)
                    return JsonResponse({"ok":"ok"},status=200)
                
            else:
                return JsonResponse({"error":"Fichier incorrect"},status=406)
            
    except Exception as e:
        print("erreur :", e)
        return JsonResponse({"error": "Erreur serveur"},status=500)
        
def pretraitement(request):
    """
    traite le fichier qui vient d'être upload
    parametre:
        aucun
    retour:
        
    """
    if request.method=="PUT":
            if "a_traiter.csv" not in os.listdir("./donnees_a_traiter"):
                return JsonResponse({"error" : "Veuillez upload un fichier avant"}, status=404)
            
            data=json.loads(request.body.decode('utf-8'))
            compte=data.get("compte")
            [doublons,dateInvalides,cheminDates,cheminDoublons]=m.pretraitement("./donnees_a_traiter/a_traiter.csv",compte)
            cheminDates=Domaine+cheminDates
            cheminDoublons=Domaine+cheminDoublons
            if not doublons.empty and not dateInvalides.empty:
                return JsonResponse({"warning": "des doublons et des dates incorrectes ont été  détectées (transaction ajoutée plus vieille que la dernière enregistrée)","df":cheminDates,"df2":cheminDoublons},status=200)
            if not doublons.empty:
                return JsonResponse({"warning": "Des doublons ont été détectés, ces données ont été ignorées dans le traitement","df2":cheminDoublons}, status=200)
            #l'orientation transforme le Dataframe en lise de dictionnaires (dont les clés sont les colonnes et les valeurs, les valeurs de cette ligne)
            if not dateInvalides.empty:

                return JsonResponse({"warning": "Une date des données à traiter est plus ancienne que celle des données déjà traitées, ces données ont été traitées","df":cheminDates},status=200)
            return JsonResponse({"ok":"Vous pouvez maintenant analyser les données"},status=200)    
        
        


def analyseAnnee(request):
    """
    renvoie des graphiques qui montrent à quoi ressemblent les dépenses par jour dans un mois
    paramètres:
        - annee: string
    retours:
        -chemins des images
        -nom des images
    
    """
    if request.method=="POST":
        try:
            data=json.loads(request.body.decode('utf-8'))
            annee=data.get("annee") 
            compte=data.get("compte")
            nonErr,gain,depenses,bilan=a.AnalyseAnnee(annee,compte) #ici l'année est un string
            if compte is None:
                compte=""
            else:
                compte+="/"
            if not nonErr:
                return JsonResponse({"error": "une erreur est survenue"},status=500)
            else:
                chem=f"{Domaine}exports/{compte}{annee}"
                
                chemins=[f"{chem}/Depenses_{annee}.jpg",f"{chem}/Gains_{annee}.jpg",f"{chem}/Bilan_{annee}.jpg"]
                return JsonResponse({"chemins":chemins,"noms":[f"Depenses {annee}", f"Gains {annee}", f"Bilan {annee}"],"bilan":[depenses,gain,bilan]},status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=406)
    

def analyseMois(request):
    """
    renvoie des graphiques qui montrent à quoi ressemblent les dépenses par jour dans un mois
    paramètres:
        - mois: string
        - annee: string
    retours:
        -chemins des images
        -nom des images
    """
    if request.method=="POST":
        try:
            data=json.loads(request.body.decode('utf-8')) #ce n'est pas un fichier qui est envoyé donc il faut décoder
            annee=data.get("annee") 
            mois=data.get("mois")
            compte=data.get("compte")
            nonErr,gain,depenses,bilan=a.AnalyseMois(annee,mois,compte)
            if compte is None:
                compte=""
            else:
                compte+="/"
            if not nonErr:
                return JsonResponse({"error": "une erreur est survenue"},status=500)
            else:
                chem=f"{Domaine}exports/{compte}{annee}/{mois}_{annee}"
                chemins=[f"{chem}/Depenses_{mois}_{annee}.jpg",f"{chem}/Gains_{mois}_{annee}.jpg",f"{chem}/Bilan_{mois}_{annee}.jpg"]
                return JsonResponse({"chemins":chemins,"noms":[f"Depenses {mois} {annee}", f"Gains {mois} {annee}", f"Bilan {mois} {annee}"],"bilan":[depenses,gain,bilan]},status=200)
        except json.JSONDecodeError as e:
            print("erreur JSON :",e)
            return JsonResponse({"error": "JSON Invalide"},status=400)
        except Exception as e:
            print("erreur :",e)
            return JsonResponse({"error":"une erreur est survenue"},status=500)
    pass

def somme(request):
    """
    renvoie la somme selon une colonne après avoir peut-être filtré le dataframe
    """
    if request.method=="POST":
        try:
            data=json.load(request.body)
            criteres=data.get("criteres") #critere: {clé:(valeur,strict)} ou la clé est une colonne du DataFrame, valeur est une valeur que ça peut prendre et strict est utile pour les chaines (si strict: == sinon substring)
            colonnes=data.get("colonnes") #colonnes dont on veut obtenir la somme liste [] Chaque colonne doit être dans le DataFrame
            compte=data.get("compte")
            df,doublon=m.importPasse(compte)
            df=a.filtre(df,criteres)
            sortie={colonne: df[colonnes].sum() for colonne in colonnes}
            return JsonResponse(sortie, status=200)


        except json.JSONDecodeError as e:
            return JsonResponse({"error": "JSON Invalide"},status=400)
    
def get_columns(request):
    """
    renvoie la liste des colonnes présentes dans le dataframe enregistré
    """
    if request.method=="GET":
        try:
            compte=data.get("compte")
            df=m.importPasse(compte)
            data=[col for col in df.columns]
            return JsonResponse({"data":data},status=200)
        except Exception as e:
            print("Une erreur est survenue:",e)
            return JsonResponse({"error":"Erreur serveur"},status=500)
# Create your views here.
def comptes(request):
    """renvoie la liste des comptes actuellement enregistrés"""
    if request.method=="GET":

            comptes= [compte for compte in os.listdir("./exports")]
            return JsonResponse({"comptes":comptes},status=200)

def creeCompte(request):
    """Crée le dossier correspondant au nouveau compte""" 
    if request.method=="POST":
        try:
            data=json.loads(request.body.decode("utf-8"))
            compte=data.get("compte")
            os.makedirs(f"./exports/{compte}",exist_ok=True)
            return JsonResponse({"ok":"compte créé"},status=200)
        except Exception as e:
            print("Erreur: ",e)
            return JsonResponse({"error":"Erreur serveur"},status=500)
def filtre(request): #on affichera le DF en forme de tableau seulement pour les entrées correspondantes au critère
    pass    
def calcImpots(request): #probablement compliqué 
    pass

def verify(request): #vérifie que les données enregistrées correspondent aux données de la banque jusqu'à la date de la dernière donnée enregistrée
    #permet de détecter aisément une incohérence
    if request.method=="POST":
            data=json.loads(request.body.decode("utf-8"))
            print(data)
            compte=data.get("compte")
            print("compte, ",compte)
            fichier="./donnees_a_traiter/a_traiter.csv"
            cheminPasse,cheminFichier,ProblemePasse,problemeFichier=a.verification(fichier,compte)
            if cheminPasse==False and cheminFichier==False and ProblemePasse==False and problemeFichier==False:
                return JsonResponse({"error":"Veuillez d'abord importer des fichiers de référence"},status=404)
            cheminPasse=Domaine+cheminPasse
            cheminFichier=Domaine+cheminFichier
            return JsonResponse({"cheminPasse":cheminPasse,"cheminFichier":cheminFichier,"problemePasse":ProblemePasse,"problemeFichier":problemeFichier},status=200)
        
def camembert(request): #voir la répartition des dépenses
    pass
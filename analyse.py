import main as m
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def sauvegarderFigures(df:pd.DataFrame,titre:str,chemin):
    plt.figure()
    df.plot(kind="bar")
    plt.title(titre)
    plt.savefig(f"./exports/{chemin}.jpg")

def AnalyseAnnee(annee:str):

    pass

def AnalyseMois(Annee:str,Mois:str): 
    MoisAnnee=f"{Mois}_{Annee}"
    fichier=f"./exports/{Annee}/{MoisAnnee}/{MoisAnnee}.csv"
    df=m.importer(fichier,0) #ce df est le bilan débit + recettes
    df["Date de comptabilisation"]=df["Date de comptabilisation"].apply(lambda s: int(s.strftime("%d")))
    df["Bilan"]=df["Credit"].fillna(0)+df["Debit"].fillna(0)

    bilan=df[["Date de comptabilisation","Bilan"]]
    bilanParJour=bilan.groupby("Date de comptabilisation")["Bilan"].sum()
    depenses=df[df["Debit"].notna()] 
    depenses["Debit"]=depenses["Debit"].apply(lambda x: abs(x))
    depenses.sort_values("Debit",inplace=True)
    depensesparjour=depenses.groupby("Date de comptabilisation")["Debit"].sum()
    gain=df[df["Credit"].notna()]
    gain.sort_values("Credit",inplace=True)
    print(gain["Credit"])
    gainparjour=gain.groupby("Date de comptabilisation")["Credit"].sum()
    sauvegarderFigures(depensesparjour,"Depenses par jour",f"{Annee}/{MoisAnnee}/Depenses_{MoisAnnee}")
    sauvegarderFigures(gainparjour, "Gain par Jour",f"{Annee}/{MoisAnnee}/Gains_{MoisAnnee}")
    
    sauvegarderFigures(bilanParJour,"Bilan par jour",f"{Annee}/{MoisAnnee}/Bilan_{MoisAnnee}")
    print(gain["Credit"].sum())
    print(depenses["Debit"].sum())
    print(bilan["Bilan"].sum())


date="01_2024"

AnalyseMois("2024","01")
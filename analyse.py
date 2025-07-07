import main as m
import matplotlib.pyplot as plt
import pandas as pd
import os
def sauvegarderFigures(df:pd.DataFrame,titre:str,chemin):
    plt.figure()
    dfCopy=df.copy().astype(float)
    dfCopy.plot(kind="bar")
    plt.title(titre)
    plt.savefig(f"{chemin}.jpg")

def AnalyseAnnee(annee:str)->bool:
    """
    annee: YYYY
    affiche et sauvegarde des graphiques des dépenses par mois, crédits par mois et bilan par mois
    return True si le traitement a réussi, False sinon 

    """
    dfs=[]
    if annee not in os.listdir("./exports"):
        print("Dossier inexistant")
        return False
    for dossier in os.listdir(f"./exports/{annee}"):
        if "." in dossier: continue #on ignore les éventuels fichiers présents ici
        for fichier in os.listdir(f"./exports/{annee}/{dossier}"):
            if ".csv" in fichier: #on garde que les csv
                dfs.append(m.importer(f"./exports/{annee}/{dossier}/{fichier}",0))
    
    df,dfD=m.concatener(dfs)
    chemin=f"./exports/{annee}"
    traitement(df,chemin,annee,"Annee")
    return True

def traitement(df:pd.DataFrame,chemin:str,nom:str,typ:str):
    if typ=="Mois":

        df["Date de comptabilisation"]=df["Date de comptabilisation"].apply(lambda s: int(s.strftime("%d"))) #si on veut le bilan du mois on plot par jour
    elif typ=="Annee":
        df["Date de comptabilisation"]=df["Date de comptabilisation"].apply(lambda s: int(s.strftime("%m")))#si on veut le bilan de l'année on plot par mois
    df["Bilan"]=df["Credit"].fillna(0)+df["Debit"].fillna(0)

    bilan=df[["Date de comptabilisation","Bilan"]]
    bilanParJour=bilan.groupby("Date de comptabilisation")["Bilan"].sum()
    depenses=df[df["Debit"].notna()] 
    depenses["Debit"]=depenses["Debit"].apply(lambda x: abs(x))
    depenses.sort_values("Debit",inplace=True)
    depensesparjour=depenses.groupby("Date de comptabilisation")["Debit"].sum()
    gain=df[df["Credit"].notna()]
    gain.sort_values("Credit",inplace=True)
    if typ=="Mois":
        a="Depenses par jour"
        b="Gain par jour"
        c="Bilan par jour"
    elif typ=="Annee":
        a="Depenses par mois"
        b="Gain par mois"
        c="Bilan par mois"
    gainparjour=gain.groupby("Date de comptabilisation")["Credit"].sum()
    sauvegarderFigures(depensesparjour,a,f"{chemin}/Depenses_{nom}")
    sauvegarderFigures(gainparjour, b,f"{chemin}/Gains_{nom}")
    
    sauvegarderFigures(bilanParJour,c,f"{chemin}/Bilan_{nom}")
    print("Gains pour", nom,":",gain["Credit"].sum())
    print("Depenses pour",nom,":",depenses["Debit"].sum())
    print("Bilan pour",nom,":",bilan["Bilan"].sum())

def AnalyseMois(Annee:str,Mois:str)->bool: #annee YYYY mois mm
    """
    annee: YYYY
    mois: mm

    affiche et sauvegarde des graphiques des dépenses par jour, crédits par jour et bilan (crédit - dépenses) par jour
    """
    MoisAnnee=f"{Mois}_{Annee}"
    fichier=f"./exports/{Annee}/{MoisAnnee}/{MoisAnnee}.csv"
    try:
        df=m.importer(fichier,0) #ce df est le bilan débit + recettes
    except Exception as e:
        print(e)
        return False
    chemin=f"./exports/{Annee}/{MoisAnnee}"
    traitement(df,chemin,MoisAnnee,"Mois")
    return True

def filtre(df:pd.DataFrame,libelle:str,mois=None)->pd.DataFrame:
    """
    on affiche que les résultats du df qui correspondent au libelle et au mois s'il est précisé
    
    """
    res=df[df["Libelle"]==libelle]
    if mois is not None:
        mois=datetime.strptime("%m_%Y")
        res=res[res["Date de comptbilisation"]==mois]
     return res

if __name__=="__main__":
    AnalyseAnnee("2025")
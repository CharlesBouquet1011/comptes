import matplotlib
matplotlib.use('Agg') #changement du backend de plot, pas de TKinter (ça fait crash django) mais Anti Grain Geometry
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime

def sauvegarderFigures(df:pd.DataFrame,titre:str,chemin):
    dfCopy = df.copy().astype(float)
    ax = dfCopy.plot(kind="bar", figsize=(5, 3))  
    ax.set_title(titre)
    plt.tight_layout()
    plt.savefig(f"{chemin}.jpg", dpi=150) #le DPI est utile pour que l'image ne soit pas entièrement blanche (jsp pourquoi ça bug sans alors que c'est le paramètre par défaut normalement)
    plt.close()

def AnalyseAnnee(annee:str,compte)->bool:
    from . import main as m

    """
    annee: YYYY
    affiche et sauvegarde des graphiques des dépenses par mois, crédits par mois et bilan par mois
    return True si le traitement a réussi, False sinon 

    """
    dfs=[]
    if compte is None:
        compte=""
    else:
        compte+="/"
    if annee not in os.listdir(f"./exports/{compte}"):
        print("Dossier inexistant")
        return False,0,0,0
    for dossier in os.listdir(f"./exports/{compte}{annee}"):
        if "." in dossier: continue #on ignore les éventuels fichiers présents ici
        for fichier in os.listdir(f"./exports/{compte}{annee}/{dossier}"):
            if ".csv" in fichier: #on garde que les csv
                dfs.append(m.importer(f"./exports/{compte}{annee}/{dossier}/{fichier}",0))
    
    df,dfD,chemin2=m.concatener(dfs)
    chemin=f"./exports/{compte}{annee}"
    gain,depenses,bilan=traitement(df,chemin,annee,"Annee")
    return True,gain,depenses,bilan

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
    return gain["Credit"].sum(),depenses["Debit"].sum(),bilan["Bilan"].sum()
def AnalyseMois(Annee:str,Mois:str,compte)->bool: #annee YYYY mois mm

    """
    annee: YYYY
    mois: mm

    affiche et sauvegarde des graphiques des dépenses par jour, crédits par jour et bilan (crédit - dépenses) par jour
    """
    from . import main as m
    if compte is None:
        compte=""
    else:
        compte+="/"
    MoisAnnee=f"{Mois}_{Annee}"
    fichier=f"./exports/{compte}{Annee}/{MoisAnnee}/{MoisAnnee}.csv"
    try:
        df=m.importer(fichier,0) #ce df est le bilan débit + recettes
    except Exception as e:
        print(e)
        return False
    chemin=f"./exports/{compte}{Annee}/{MoisAnnee}"
    gain,depenses,bilan=traitement(df,chemin,MoisAnnee,"Mois")
    return True,gain,depenses,bilan

def filtreparLibelle(df:pd.DataFrame,libelle:str,mois=None)->pd.DataFrame:
    """
    on affiche que les résultats du df qui correspondent au libelle et au mois s'il est précisé
    recherche large (le libellé correspond en partie à la ligne du dataframe)
    
    """
    res=df[df["Libelle simplifie"].str.contains(libelle,na=False)]
    if mois is not None:
        mois=datetime.datetime.strptime("%m_%Y")
        res=res[res["Date de comptabilisation"]==mois]
    return res

def filtre(df:pd.DataFrame,criteres:dict[tuple[str,bool]]):
    for crit,tuple in criteres.items():
        val,strict=tuple
        if strict:
            df=df[df[crit]==val]
        else:
            df=df[df[crit.str.contains(val,na=False)]]
    return df

def verification(fichier,compte):
    """
    le fichier doit contenir TOUTES les transactions du compte/des comptes (déconseillé de faire tous les comptes mais pris en charge)
    Vérifie que chaque entrée dans le df du fichier a une correspondance dans les DF enregistrés et inversement
    """
    from . import main as m
    
    df=m.importer(fichier,3)
    df["source"]="fichier"
    
    dfPasse,dfPasseDoublon=m.importPasse(compte)
    if dfPasse.empty or dfPasse.isna().all(axis=None):
        return False,False,False,False #il faudra retourner une erreur ici


    df.reset_index(inplace=True)
    dfPasse.reset_index(inplace=True)
    dfPasse["source"]="passe"
    full=pd.concat([df,dfPasse],join="outer",axis=0,ignore_index=True)
    doublons=full.duplicated(keep=False,subset=full.columns.difference(["source"]))
    uniques=full[~doublons]
    uniques.set_index('Reference',inplace=True)
    uniquePasse=uniques[uniques["source"]=="passe"]
    uniquesFichier=uniques[uniques["source"]=="fichier"]
    uniquePasse.drop(axis=1,inplace=True,columns=["source"])
    uniquesFichier.drop(axis=1,inplace=True,columns=["source"])
    chemin=f"./verification/{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')}"
    os.makedirs(chemin,exist_ok=True)
    chemin1=f"{chemin}/local.xlsx"
    chemin2=f"{chemin}/fichier.xlsx"
    problemePasse=not uniquePasse.empty
    problemeFichier=not uniquesFichier.empty
    if problemePasse:
        with pd.ExcelWriter(chemin1,engine="xlsxwriter",date_format="%d/%m/%Y") as writer:
            uniquePasse.to_excel(writer)
    if problemeFichier:
        with pd.ExcelWriter(chemin2,engine="xlsxwriter",date_format="%d/%m/%Y") as writer:
            uniquesFichier.to_excel(writer)

    return chemin1,chemin2,problemePasse,problemeFichier


if __name__=="__main__":
    AnalyseAnnee("2025")
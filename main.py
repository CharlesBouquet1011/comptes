import pandas as pd
import os
import datetime
from erreurs import IncorrectDate,Duplicates
from decimal import Decimal #pour virer les problèmes d'arrondi de virgule flottante
import analyse as a
def convertisseur(s):
    if pd.isna(s): #on n'y touche pas
        return s
    if type(s)==Decimal:
        return s
    s=str(s) #on s'assure que c'est un string pour éviter des bugs
    if "-" in s:
            signe=-1
    else:
        signe=1
    if "-" in s or "+" in s:
        s=s[1:]
        
    s=s.replace(",",".") #on ne peut pas convertir des nombres à virgules avec float, il faut des .
    return signe*Decimal(s)


def importer(fichier,ind): #chemin du fichier
    try:
        df=pd.read_csv(fichier,sep=";",index_col=ind)
    except Exception as e:
        print("Erreur lors de l'ouverture du fichier: ", e)
        return pd.DataFrame()
    df["Date de comptabilisation"]=pd.to_datetime(df["Date de comptabilisation"],errors='coerce',format='%d/%m/%Y')
    df["Date de valeur"]=pd.to_datetime(df["Date de valeur"],errors='coerce',format='%d/%m/%Y')
    
    df["Debit"]=df["Debit"].apply(lambda s: convertisseur(s))
    df["Credit"]=df["Credit"].apply(lambda s: convertisseur(s))
    return df

def initialisation():
    os.makedirs("./doublons",exist_ok=True)
    os.makedirs("donnees_a_traiter",exist_ok=True)
    os.makedirs("DatesIncorrectes",exist_ok=True)
    os.makedirs("./exports",exist_ok=True)

def importPasse():
    
    
    #exports=os.listdir('./exports')
    #dfpasses=[importer('./exports/'+i,0) for i in exports] #référence passe en index (colonne 0) dans les enregistrements
    dfpasses=[]
    for dossier in os.listdir("./exports"):
        for sousDos in os.listdir(f"./exports/{dossier}"):
            if "." in sousDos: continue #on ignore les éventuels fichiers présents ici
            for fichier in os.listdir(f"./exports/{dossier}/{sousDos}"):
                if ".csv" in fichier: #on garde seulement les fichiers csv
                    dfpasses.append(importer(f"./exports/{dossier}/{sousDos}/{fichier}",0))

    
    
    if not dfpasses:
        return pd.DataFrame(),pd.DataFrame()
    df,dfDoublon=concatener(dfpasses)
    
    return df,dfDoublon

def concatener(liste_df:list[pd.DataFrame]):
    liste_del=[]
    for i in range(len(liste_df)) :
        df=liste_df[i]
        df.reset_index(inplace=True)
        if df.empty or df.isna().all(axis=None):
            liste_del.append(i) #si le df est vide ou alors contient que des NaN, on le marque pour suppression
    for i in liste_del[::-1]: #on inverse pour pas changé l'index des futurs df à supprimer
        liste_df.pop(i) #on supprime les df marqués
    dftemp=pd.concat(liste_df,axis=0,ignore_index=True,join='outer')
    doublons=dftemp.duplicated(keep=False) #subset = None quand on vérifie les duplications sur l'index
    df_doublons=dftemp[doublons]
    uniques=dftemp.drop_duplicates(ignore_index=True)
    uniques.set_index('Reference',inplace=True)
    if not df_doublons.empty:
        print("""
            !!!!
    ATTENTION, Des doublons ont été détectés dans les comptes passés
    !!!!        
    """)
        df_doublons.to_csv("./doublons/"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')+".csv",sep=";",date_format="%d/%m/%Y")
        ans=input("Souhaitez vous continuer tout de même ? (ces données seront ignorées et visibles dans une fichier à part) (oui/non)")
        ans=ans.lower()
        if ans!="oui":
            raise Duplicates("Des références en double ont été détectées, voir dossier doublons")
    return uniques,df_doublons
    #à gauche, ce qu'on veut garder (pas les doublons), à droite ce qu'on a drop (les lignes problématiques)

def verifDates(df:pd.DataFrame,dfpasse:pd.DataFrame): #si pas de problem, df vide, sinon df pas vide
    """
    Vérifie que la dernière date du passé soit plus vieille que la première date du présent (sinon il y a un problème)
    """ 
    if dfpasse.empty: #il n'y a pas de données passées
        return pd.DataFrame()
    date_plus_recente_passee=dfpasse["Date de comptabilisation"].max()
    dfproblem=df[df["Date de comptabilisation"]<=date_plus_recente_passee]
    if not dfproblem.empty:
        print("""
            !!!!
              Attention, des données antérieures à la date la plus récente des transactions passées a été détectée

              !!!!!
""")
        dfproblem.to_csv("./DatesIncorrectes/"+datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')+".csv",sep=";",date_format="%d/%m/%Y")
        ans=input("Souhaitez vous continuer tout de même ? (ces données seront ignorées et visibles dans une fichier à part) (oui/non)")
        ans=ans.lower()

        if ans!="oui":
            
            raise IncorrectDate("Des dates incorrectes ont été détectées, voir dossier DatesIncorrectes")
    return dfproblem

def Export(df:pd.DataFrame):
    """
    Exporte les données par mois dans des csv
    
    """
    dateDebut=df["Date de comptabilisation"].min()
    dateFin=df["Date de comptabilisation"].max()
    anneeDebut=int(dateDebut.strftime("%Y"))
    moisDebut=int(dateDebut.strftime("%m"))
    anneeFin=int(dateFin.strftime("%Y"))
    moisFin=int(dateFin.strftime("%m"))
    #iterer pour créer tous les df des mois (de chaque année)
    liste_df_Mois=[]
    annee=anneeDebut
    mois=moisDebut
    while annee<anneeFin or (annee==anneeFin and mois<=moisFin):
        while mois<13:
            
            debutMois=datetime.datetime(year=annee,month=mois,day=1)
            if mois!=12:
                moisSuivant=mois+1
                anneeSuivante=annee
            else:
                anneeSuivante=annee+1
                moisSuivant=1
            finMois=datetime.datetime(year=anneeSuivante,month=moisSuivant,day=1)
            dfMois=df[(df["Date de comptabilisation"]<finMois) & (df["Date de comptabilisation"]>=debutMois)]
            liste_df_Mois.append(dfMois)
            mois=str(mois)
            if len(mois)<2:
                mois="0"+mois
            timestamp=mois+"_"+str(annee)

            os.makedirs(f"./exports/{annee}/{timestamp}",exist_ok=True)
            dfMois.to_csv("./exports/"+str(annee)+"/"+timestamp+"/"+timestamp+".csv",sep=";",date_format="%d/%m/%Y")
            mois=int(mois)
            mois+=1
        annee+=1
        mois=1
    return liste_df_Mois

def p1(fichier):
    """
    importe et met en forme le fichier dans l'archive
    """

    df1=importer(fichier,3)
    dfpasse,dfpasseDoublons=importPasse()
    dfproblemDate=verifDates(df1,dfpasse)
    dftot,doublons=concatener([df1,dfpasse])
    Export(dftot)

def interfaceConsole():
    ans=input("Voulez vous importer des fichiers pour traitement futur ? \n")
    if ans.lower()=="oui": #import de fichiers
        print("Mettez le fichier dans le dossier 'donnees_a_traiter'")
        nom=input("Rentrez le nom du fichier CSV sans l'extension \n")
        chemin=f"./donnees_a_traiter/{nom}.csv"
        p1(chemin)
        print("vos fichiers séparés par mois sont maintenant dans ./exports, vous pouvez désormais les traiter")
    
    
    ans=input("Voulez vous Analyser vos fichiers ? (oui/non) Le traitement nécessite d'avoir préalablement importé des fichiers\n")
    if ans.lower()=="oui": #analyse des fichiers exportés préalablement
        if len(os.listdir("./exports"))==0:
            print("Veuillez préalablement importer des fichiers")
            return False #erreur
        ans=input("Voulez vous analyser par mois ou par année ? (mois/annee) \n")
        if ans.lower()=="mois":
            mois=input("Choisissez le mois (sous la forme mm_YYYY) \n")
            mois,annee=mois.split("_")
            if not a.AnalyseMois(annee,mois):
                print("une erreur inconnue est survenue, veuillez réessayer")
                return False
            print(f"vous retrouverez les bilans, depenses et gains du mois {mois}_{annee} dans le dossier ./exports/{annee}/{mois}_{annee}")
        elif ans.lower()=="annee":
            annee=input("Choisissez l'année (sous la forme YYYY) \n")

            if not a.AnalyseAnnee(annee):
                print("une erreur inconnue est survenue, veuillez réessayer")
                return False
            print(f"Vous retrouverez les bilans, depenses et gains de l'année{annee} dans le fichier ./exports{annee}")
    return True

def main():
    initialisation()
    interfaceConsole()


    












if __name__=="__main__":
    main()

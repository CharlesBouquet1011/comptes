import pandas as pd
import os
import datetime
from erreurs import IncorrectDate,Duplicates

def convertisseur(s):
    if pd.isna(s): #on n'y touche pas
        return s
    if type(s)==float:
        return s
    if "-" in s:
            signe=-1
    else:
        signe=1
    if "-" in s or "+" in s:
        s=s[1:]
        
    s=s.replace(",",".") #on ne peut pas convertir des nombres à virgules avec float, il faut des .
    return signe*float(s)


def importer(fichier,ind): #chemin du fichier
    df=pd.read_csv(fichier,sep=";",index_col=ind)
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
            for fichier in os.listdir(f"./exports/{dossier}/{sousDos}"):
                if ".csv" in fichier:
                    dfpasses.append(importer(f"./exports/{dossier}/{sousDos}/{fichier}",0))

    
    
    if not dfpasses:
        return pd.DataFrame(),pd.DataFrame()
    df,dfDoublon=concatener(dfpasses)
    
    return df,dfDoublon

def concatener(liste_df:list[pd.DataFrame]):
    for df in liste_df:
        df.reset_index(inplace=True)
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
    initialisation()

    df1=importer(fichier,3)
    dfpasse,dfpasseDoublons=importPasse()
    dfproblemDate=verifDates(df1,dfpasse)
    dftot,doublons=concatener([df1,dfpasse])
    Export(dftot)




def main():
    p1("donnees_a_traiter\\05072025_949414.csv")


    












if __name__=="__main__":
    main()

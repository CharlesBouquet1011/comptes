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
        comptes=[compte+"/" for compte in os.listdir("./exports") if "." not in compte and compte!="tousComptes"]
        chemin=f"./exports/tousComptes/{annee}"
        os.makedirs(chemin,exist_ok=True) #il n'y a pas eu la fonction prétraitement qui a créé le dossier pour ce cas là
    else:
        compte+="/"
        comptes=[compte]
        chemin=f"./exports/{compte}{annee}"
        if annee not in os.listdir(f"./exports/{compte}") and len(comptes)==1:
            print("Dossier inexistant")
            return False,0,0,0,0
    for compte in comptes:
        if annee not in os.listdir(f"./exports/{compte}"): continue
        for dossier in os.listdir(f"./exports/{compte}{annee}"):
            if "." in dossier: continue #on ignore les éventuels fichiers présents ici
            for fichier in os.listdir(f"./exports/{compte}{annee}/{dossier}"):
                if ".csv" in fichier: #on garde que les csv
                    dfs.append(m.importer(f"./exports/{compte}{annee}/{dossier}/{fichier}",0))
    
    df,dfD,chemin2=m.concatener(dfs)
    
    gain,depenses,bilan=traitement(df,chemin,annee,"Annee")
    return True,gain,depenses,bilan,chemin

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
        d="Repartition depenses par mois"
        e="Repartition gains par mois"
    elif typ=="Annee":
        a="Depenses par mois"
        b="Gain par mois"
        c="Bilan par mois"
        d="Repartition depenses par an"
        e="Repartition gains par an"
    gainparjour=gain.groupby("Date de comptabilisation")["Credit"].sum()
    sauvegarderFigures(depensesparjour,a,f"{chemin}/Depenses_{nom}")
    sauvegarderFigures(gainparjour, b,f"{chemin}/Gains_{nom}")
    
    sauvegarderFigures(bilanParJour,c,f"{chemin}/Bilan_{nom}")
    
    
    
    depensesparLib=depenses.groupby("Libelle simplifie")["Debit"].sum() #ATTENTION le groupby renvoie une SERIES pas un DATAFRAME (donc pour rajouter une entrée dans la series c'est la même syntaxe que pour rajouter une colonne dans un df)
    gainparLib=gain.groupby("Libelle simplifie")["Credit"].sum()

        
    Figurecamembert(depensesparLib,d,f"{chemin}/Repartition_Depenses_{nom}")
    Figurecamembert(gainparLib,e,f"{chemin}/Repartition_Gains_{nom}")


    return gain["Credit"].sum(),depenses["Debit"].sum(),bilan["Bilan"].sum()
def AnalyseMois(Annee:str,Mois:str,compte)->bool: #annee YYYY mois mm

    """
    annee: YYYY
    mois: mm

    affiche et sauvegarde des graphiques des dépenses par jour, crédits par jour et bilan (crédit - dépenses) par jour
    """
    from . import main as m
    MoisAnnee=f"{Mois}_{Annee}"
    try:
        if compte is None:
            compte="tousComptes/"
            fichiers=[f"./exports/{c}/{Annee}/{MoisAnnee}/{MoisAnnee}.csv" for c in os.listdir("./exports") if "." not in c and c!="tousComptes"]
            dfs=[m.importer(fichier,0) for fichier in fichiers]
            df,doublons,cheminDoublon=m.concatener(dfs)
            chemin=f"./exports/tousComptes/{Annee}/{MoisAnnee}"
            os.makedirs(chemin,exist_ok=True)
        else:
            compte+="/"
            fichier=f"./exports/{compte}{Annee}/{MoisAnnee}/{MoisAnnee}.csv"
            df=m.importer(fichier,0) #ce df est le bilan débit + recettes
            chemin=f"./exports/{compte}{Annee}/{MoisAnnee}"

        gain,depenses,bilan=traitement(df,chemin,MoisAnnee,"Mois")
        return True,gain,depenses,bilan,chemin
    except Exception as e:
            print("Erreur: ",e)
            return False,0,0,0,0

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
    if compte is None:
        comptes=[compte for compte in os.listdir("./exports") if "." not in compte and compte!="tousComptes"]
        dfPasses=[m.importer(compte)[0] for compte in comptes]
        dfPasse,dfPasseDoublon,chemindfpassesDoublons=m.concatener(dfPasses)
    else:    
        dfPasse,dfPasseDoublon=m.importPasse(compte)
        if dfPasse.empty or dfPasse.isna().all(axis=None):
            return False,False,False,False #il faudra retourner une erreur ici
    
    
    
    dfPasse.reset_index(inplace=True)
   
    df.reset_index(inplace=True)
    
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

def Figurecamembert(df, titre, chemin, legende_separee=True):
    """
    Met en forme les données et les affiches sous forme de diagramme camembert, la mise en page (couleurs,police,légende) est faite par IA parce que j'avais la flemme et que je suis pas designer
    
    """
    dfCopy = df.copy().astype(float)
    
    dfCopy = dfCopy.sort_values(ascending=False)
    
    # Regrouper les petites valeurs (< 2%) dans "Autres"
    seuil = 2.0
    petites_valeurs = dfCopy[dfCopy < seuil]
    grandes_valeurs = dfCopy[dfCopy >= seuil]
    
    if len(petites_valeurs) > 0:
        autres_valeur = petites_valeurs.sum()
        grandes_valeurs['Autres'] = autres_valeur
        dfCopy = grandes_valeurs
    
    # Générer des couleurs distinctes
    colors = plt.cm.Set3(range(len(dfCopy)))
    
    # ========== GRAPHIQUE PRINCIPAL ==========
    fig, ax = plt.subplots(figsize=(4, 4), dpi=150)
    
    # Créer le camembert
    wedges, texts, autotexts = ax.pie(
        dfCopy.values,
        labels=None,  
        autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
        startangle=90,
        counterclock=False,
        colors=colors,
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    
    # Améliorer la visibilité des pourcentages
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Titre
    ax.set_title(titre, fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f"{chemin}.jpg", dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    # ========== LÉGENDE SÉPARÉE ==========
    if legende_separee:
        CreerLegendeManuelle(dfCopy, colors, f"{chemin}_legende")

        #_creer_legende_separee(dfCopy, colors, f"{chemin}_legende")



if __name__=="__main__":
    AnalyseAnnee("2025")


# Alternative : Version manuelle avec dessin pixel par pixel
def CreerLegendeManuelle(dfCopy, colors, chemin_legende):
    """Version manuelle qui dessine pixel par pixel - ZERO blanc garanti (fait par IA)"""
    
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    
    total = dfCopy.sum() if hasattr(dfCopy, 'sum') else sum(dfCopy.values())
    
    # Paramètres
    font_size = 12
    line_height = 18
    color_box_size = 14
    text_margin = 8
    
    # Calculer dimensions exactes
    labels = []
    for i, (label, value) in enumerate(dfCopy.items()):
        pct = (value / total) * 100
        labels.append(f'{label} ({pct:.1f}%)')
    
    # Estimer la largeur du texte (approximation)
    max_text_width = max(len(label) for label in labels) * 7  # ~7px par caractère
    
    width = color_box_size + text_margin + max_text_width + 10
    height = len(labels) * line_height + 10
    
    # Créer l'image
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Essayer de charger une police (fallback sur police par défaut)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Dessiner chaque élément de légende
    y_pos = 5
    for i, (label, color) in enumerate(zip(labels, colors)):
        # Convertir couleur matplotlib en RGB
        if hasattr(color, '__len__') and len(color) >= 3:
            rgb_color = tuple(int(c * 255) for c in color[:3])
        else:
            rgb_color = (128, 128, 128)  # Gris par défaut
        
        # Dessiner le carré de couleur
        draw.rectangle([5, y_pos, 5 + color_box_size, y_pos + color_box_size], 
                      fill=rgb_color, outline='black', width=1)
        
        # Dessiner le texte
        text_x = 5 + color_box_size + text_margin
        draw.text((text_x, y_pos), label, fill='black', font=font)
        
        y_pos += line_height
    
    # Sauvegarder
    img.save(f"{chemin_legende}.jpg", quality=95, optimize=True)
    print(f"Légende manuelle créée : {chemin_legende}.jpg ({width}x{height}px)")

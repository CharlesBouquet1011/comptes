# Lancement
- installez Docker
- ouvrez un terminal à la racine du projet et écrivez `docker-compose up -d`
- allez maintenant dans votre navigateur et écrivez localhost dans la barre d'adresse

# Utilisation

Suivez les instructions indiquées à l'écran pour pouvoir analyser votre compte.

- Attention, pour analyser les comptes pour la première fois, veuillez télécharger depuis votre banque l'intégralité de vos transactions au format csv et les importer dans sur le drag and drop. Vous pourrez ensuite ajouter les nouvelles transactions au fur et à mesure. 
- Pour vérifier qu'il n'y a pas d'erreur entre vos comptes et ceux de la banque, veuillez importer encore une fois toutes les données de la banque afin de les comparer avec les données en local
- Ce logiciel suppose que vous vérifiez les montants payés au fur et à mesure des transactions, il indiquera donc simplement les incohérences si la banque fait une erreur et peut vous permettre de retrouver des dépenses chez un créditeur suspect.

# Fonctionnalités:

- Analyse graphique d'un ou de plusieurs comptes en format csv (dépenses ou gains par mois/par jour, répartition des dépenses ou des gains en fonction du créditeur/débiteur)
- Vérification d'incohérences entre les transactions de la banques et celles enregistrées en local et affichage de ces incohérences au format xlsx (Transactions manquantes/en trop, nouvelles transactions qui apparaissent dans le passé)

# Limitations
Ce logiciel calcule automatiquement les bilans bancaires (indique s'il y a des doublons de virements ou des virements effectués dans le passé mais pas présent dans les fichiers du pc en local) mais ne peut en aucun cas vérifier si vous avez été prélevé plus que nécessaire sur un paiement que vous avez effectué, vous devez vérifier cela vous-mêmes au préalable.

# Librairies
## backend
- pandas
- django
- xlsxwriter
- matplotlib
- numpy
- os
- datetime
- PIL
- decimal

## frontend
- react (et toutes ses dépendances)
- tailwindcss
- DatetimePicker
- Dropzone

(ces librairies s'installent avec npm install)
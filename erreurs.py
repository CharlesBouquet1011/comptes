class IncorrectDate(Exception):
    """
    La date d'une transaction des données à traiter est antérieure à la date de la donnée la plus récente des données déjà traitées
    """

class Duplicates(Exception):
    """
    Des références en double ont été détectées.
    """
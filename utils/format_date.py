import os
import time

def formater_date(chemin):
    """
    Retourne une chaîne formatée représentant la date de création du fichier/dossier.
    """
    try:
        timestamp = os.path.getctime(chemin)
        return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(timestamp))
    except Exception as e:
        return "Date inconnue"

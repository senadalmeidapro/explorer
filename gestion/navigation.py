import os
import time
from gestion.operations_fichiers import custom_show_error

def lister_repertoire(chemin):
    """Liste le contenu du répertoire avec les informations des fichiers et dossiers."""
    try:
        contenu = []
        for nom in os.listdir(chemin):
            chemin_complet = os.path.join(chemin, nom)
            if os.path.isdir(chemin_complet):
                # Récupérer la date de création et de modification du dossier
                date_creation = os.path.getctime(chemin_complet)
                date_creation = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_creation))
                date_modification = os.path.getmtime(chemin_complet)
                date_modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_modification))
                contenu.append({
                    "nom": nom,
                    "type": "Dossier",
                    "taille": "",
                    "date_creation": date_creation,
                    "date_modification": date_modification
                })
            else:
                taille = os.path.getsize(chemin_complet)
                # Récupérer la date de création et de modification du fichier
                date_creation = os.path.getctime(chemin_complet)
                date_creation = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_creation))
                date_modification = os.path.getmtime(chemin_complet)
                date_modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_modification))
                contenu.append({
                    "nom": nom,
                    "type": "Fichier",
                    "taille": f"{taille} ",
                    "date_creation": date_creation,
                    "date_modification": date_modification
                })
        return contenu
    except OSError as ose:
        if ose.errno == 13:
            custom_show_error("Accès refusé", f"Accès refusé")
        else:
            custom_show_error("Erreur", f"Erreur lors de l'accès à {chemin}")
        return []
    except Exception as e:
        custom_show_error("Erreur", f"Erreur lors de l'accès à {chemin}")
        return []

import os
import time
from gestion.operations_fichiers import custom_show_error

def lister_repertoire(chemin):
    """Liste le contenu du répertoire avec les informations des fichiers et dossiers."""
    try:
        contenu = []
        with os.scandir(chemin) as entrees:
            for entree in entrees:
                try:
                    stats = entree.stat(follow_symlinks=False)
                except OSError:
                    continue

                if entree.is_dir(follow_symlinks=False):
                    date_creation = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_ctime))
                    date_modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))
                    contenu.append({
                        "nom": entree.name,
                        "type": "Dossier",
                        "taille": "",
                        "date_creation": date_creation,
                        "date_modification": date_modification
                    })
                else:
                    taille = stats.st_size
                    date_creation = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_ctime))
                    date_modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime))
                    contenu.append({
                        "nom": entree.name,
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

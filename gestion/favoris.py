import os

# Liste des favoris (en mémoire). Pour un projet sérieux, vous pouvez persister ces données dans un fichier.
favoris = set()  # Utilisation d'un set pour éviter les doublons automatiquement

def ajouter_favori(chemin):
    """Ajoute un fichier ou dossier aux favoris."""
    if os.path.exists(chemin):
        favoris.add(chemin)
    else:
        pass

def retirer_favori(chemin):
    """Supprime un fichier ou dossier des favoris."""
    if chemin in favoris:
        favoris.remove(chemin)
    else:
        pass

def lister_favoris():
    """Retourne la liste des favoris."""
    if favoris:
        for index, chemin in enumerate(favoris, start=1):
            print(f"{index}. {chemin}")
    else:
        print("Aucun favori enregistré.")
    return list(favoris)

def est_favori(chemin):
    """Vérifie si un fichier ou dossier est dans les favoris."""
    return chemin in favoris



# Ajout de la gestion de l'historique pour la navigation
recents = []
current_index = 0  # Aucun chemin enregistré initialement

def add_recents(chemin):
    global recents, current_index

    # Si on a remonté dans l'historique, on tronque la liste à l'index courant
    if current_index < len(recents) - 1:
        recents = recents[:current_index + 1]

    # Si le chemin est déjà dans l'historique, ne pas l'ajouter à nouveau
    if chemin not in recents:
        recents.append(chemin)
        current_index = len(recents) - 1  # Réinitialisation de l'index

def parcours(direction):
    global recents, current_index
    if direction == "prev":
        if current_index > 0:
            current_index -= 1
            return recents[current_index], True  # Retourne le chemin précédent et True
        else:
            return None, False  # Pas de chemin précédent, retourne False
    elif direction == "next":
        if current_index < len(recents)-1:
            current_index += 1
            return recents[current_index], True  # Retourne le chemin suivant et True
        else:
            return None, False  # Pas de chemin suivant, retourne False
    elif direction == "nexts":
        if current_index < len(recents):
            current_index += 1
            return recents[current_index], True  # Retourne le chemin suivant et True
        else:
            return None, False  # Pas de chemin suivant, retourne False
    else:
        raise ValueError("La direction doit être 'prev' ou 'next'.")


def send_recent():
    return recents
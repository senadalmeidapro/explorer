import os

# Fichier de sauvegarde des favoris
FAVORIS_FILE = "favoris.txt"

# Charger les favoris depuis le fichier
def charger_favoris():
    """Charge les favoris depuis le fichier et les stocke dans un set."""
    if not os.path.exists(FAVORIS_FILE):
        return set()
    with open(FAVORIS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines() if os.path.exists(line.strip()))

# Sauvegarder les favoris dans le fichier
def sauvegarder_favoris():
    """Écrit la liste des favoris dans le fichier."""
    with open(FAVORIS_FILE, "w", encoding="utf-8") as f:
        for chemin in favoris:
            f.write(chemin + "\n")

# Initialisation des favoris
favoris = charger_favoris()

def ajouter_favori(chemin):
    """Ajoute un fichier ou dossier aux favoris et sauvegarde la mise à jour."""
    if os.path.exists(chemin):
        favoris.add(chemin)
        sauvegarder_favoris()

def retirer_favori(chemin):
    """Supprime un fichier ou dossier des favoris et sauvegarde la mise à jour."""
    if chemin in favoris:
        favoris.remove(chemin)
        sauvegarder_favoris()

def lister_favoris():
    """Retourne et affiche la liste des favoris."""
    if favoris:
        for index, chemin in enumerate(favoris, start=1):
            print(f"{index}. {chemin}")
    else:
        print("Aucun favori enregistré.")
    return list(favoris)

def est_favori(chemin):
    """Vérifie si un fichier ou dossier est dans les favoris."""
    return chemin in favoris


# 🔹 GESTION DE L'HISTORIQUE DES DOSSIERS RÉCENTS 🔹

recents = []
current_index = 0  # Aucun chemin enregistré initialement

def add_recents(chemin):
    global recents, current_index

    # Si on a remonté dans l'historique, on tronque la liste à l'index courant
    if current_index < len(recents) - 1:
        recents = recents[:current_index + 1]

    # Ajout du chemin s'il n'est pas déjà présent
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
        if current_index < len(recents) - 1:
            current_index += 1
            return recents[current_index], True  # Retourne le chemin suivant et True
        else:
            return None, False  # Pas de chemin suivant, retourne False
    else:
        raise ValueError("La direction doit être 'prev' ou 'next'.")

def send_recent():
    return recents

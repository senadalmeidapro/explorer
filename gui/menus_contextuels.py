import os
import tkinter as tk
from gestion.favoris import ajouter_favori, retirer_favori, lister_favoris
from gestion.operations_fichiers import ouvrir_element, renommer_element, supprimer_element, creer_dossier, creer_fichier

class MenusContextuels:
    def __init__(self, parent, chemin_cible, rafraichir_callback, affichage, update_barre_callback):
        self.parent = parent
        self.chemin_cible = chemin_cible
        self.rafraichir_callback = rafraichir_callback
        self.affichage = affichage
        self.update_barre_callback = update_barre_callback

        self.menu = tk.Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Ouvrir", command=self.ouvrir)
        self.menu.add_command(label="Nouveau dossier", command=self.dossier)
        self.menu.add_command(label="Nouveau fichier", command=self.fichier)
        self.menu.add_command(label="Renommer", command=self.renommer)
        self.menu.add_command(label="Supprimer", command=self.supprimer)

        # Ajout de la gestion des favoris
        self.menu.add_separator()
        self.menu.add_command(label="Ajouter aux favoris", command=self.ajouter_aux_favoris)
        self.menu.add_command(label="Retirer des favoris", command=self.retirer_des_favoris)
        self.menu.add_command(label="Lister les favoris", command=self.lister_favoris)

    def lister_favoris(self):
        """Affiche la liste des éléments dans les favoris."""
        self.affichage.afficher_favoris()  # Appeler la méthode dans AffichageFichiers pour afficher les favoris dans l'interface

    def ouvrir(self):
        """Ouvre l'élément sélectionné (dossier ou fichier)."""
        ouvrir_element(os.path.basename(self.chemin_cible),
                       os.path.dirname(self.chemin_cible),
                       self.affichage,
                       self.update_barre_callback)

    def renommer(self):
        """Renomme l'élément sélectionné (dossier ou fichier)."""
        renommer_element(os.path.basename(self.chemin_cible),
                         os.path.dirname(self.chemin_cible))
        self.rafraichir_callback()

    def supprimer(self):
        """Supprime l'élément sélectionné (dossier ou fichier)."""
        supprimer_element(os.path.basename(self.chemin_cible),
                          os.path.dirname(self.chemin_cible))
        self.rafraichir_callback()

    def dossier(self):
        """Crée un nouveau dossier dans le répertoire sélectionné."""
        chemin = os.path.join(os.path.basename(self.chemin_cible),
                              os.path.dirname(self.chemin_cible))
        creer_dossier(chemin)
        self.rafraichir_callback()

    def fichier(self):
        """Crée un nouveau fichier dans le répertoire sélectionné."""
        chemin = os.path.join(os.path.basename(self.chemin_cible),
                              os.path.dirname(self.chemin_cible))
        creer_fichier(chemin)
        self.rafraichir_callback()

    def ajouter_aux_favoris(self):
        """Ajoute l'élément (dossier ou fichier) aux favoris."""
        if self.chemin_cible not in lister_favoris():
            ajouter_favori(self.chemin_cible)
        else:
            pass

    def retirer_des_favoris(self):
        """Retire l'élément (dossier ou fichier) des favoris."""
        if self.chemin_cible in lister_favoris():
            retirer_favori(self.chemin_cible,)
            if self.show:
                self.affichage.afficher_favoris()
                
        else:
            pass


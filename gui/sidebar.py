import customtkinter as ctk
from gui.affichage_fichiers import AffichageFichiers
from gestion.favoris import ajouter_favori, retirer_favori, lister_favoris

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, affichage, **kwargs):
        super().__init__(master, bg_color="white", width=200, **kwargs)
        self.affichage=affichage
        self.create_widgets()

    def create_widgets(self):
        # Bouton pour afficher les fichiers récents
        self.btn_recents = ctk.CTkButton(self, text="📁 Recents", fg_color="lightgrey", corner_radius=0, text_color="black",command=self.afficher_recents)
        self.btn_recents.pack(fill="x", padx=10, pady=5)

        # Bouton pour afficher les favoris
        self.btn_favorites = ctk.CTkButton(self, text="⭐ Favorites", fg_color="lightgrey", corner_radius=0, text_color="black",command=self.afficher_favorites)
        self.btn_favorites.pack(fill="x", padx=10, pady=5)

        # Bouton pour afficher la vue "Computer"
        self.btn_computer = ctk.CTkButton(self, text="💻 Computer", fg_color="lightgrey", corner_radius=0, text_color="black",command=self.afficher_computer)
        self.btn_computer.pack(fill="x", padx=10, pady=5)

    def afficher_recents(self):
        self.affichage.afficher_recents()

    def afficher_favorites(self):
        self.affichage.afficher_favoris()
        # Vous pouvez appeler la fonction lister_favoris du module gestion/favoris ici

    def afficher_computer(self):
         self.affichage.ouvrir_dossiernavc("C:/")
        # Affichage de l'ensemble des disques ou d'une vue globale

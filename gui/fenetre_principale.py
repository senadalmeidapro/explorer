import customtkinter as ctk
from gui.sidebar import Sidebar
from gui.barre_chemin import BarreChemin
from gui.affichage_fichiers import AffichageFichiers
from gestion.favoris import add_recents

class FenetrePrincipale:
    def __init__(self, master):
        self.master = master
        self.master.title("Explorateur de Fichiers")
        self.master.geometry("700x450")
        
        # Appliquer le mode d'apparence du système
        ctk.set_appearance_mode("Light")  # "System", "Dark", "Light"
        
        # Création du frame principal qui couvre toute la fenêtre
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Assurer que le frame principal s'étend avec la fenêtre
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        # Configuration des colonnes et lignes dans le frame
        self.main_frame.columnconfigure(0, weight=0)  # Sidebar fixe
        self.main_frame.columnconfigure(1, weight=1)  # Affichage fichiers prend toute la largeur restante
        self.main_frame.rowconfigure(0, weight=0)  # Barre de chemin fixe en hauteur
        self.main_frame.rowconfigure(1, weight=1)  # Affichage et sidebar prennent l'espace restant
        
        # Zone principale (ligne 1)
        self.dir = "C:/Users"
        add_recents(self.dir)
        
        # Sidebar (colonne 0, prend toute la hauteur)
        
        # Affichage des fichiers (colonne 1, prend toute la largeur restante)
        self.affichage = AffichageFichiers(
            self.main_frame,
            chemin=self.dir,
            update_barre_callback=self.mettre_a_jour_barre
        )
        self.sidebar = Sidebar(self.main_frame, self.affichage)
        self.sidebar.grid(row=1, column=0, sticky="ns", pady=10)
        # Barre de chemin (ligne 0, prend toute la largeur)
        self.barre_chemin = BarreChemin(self.main_frame, self.affichage)
        self.barre_chemin.grid(row=0, column=0, columnspan=2, sticky="ew", padx=3, pady=6)
        
        self.affichage.grid(row=1, column=1, sticky="nsew")
        
        self.barre_chemin.on_change = self.mettre_a_jour_repertoire
    
    def mettre_a_jour_repertoire(self, nouveau_chemin):
        # Remplacer les \ par des /
        nouveau_chemin = nouveau_chemin.replace("\\", "/")
        self.affichage.ouvrir_dossiernav(nouveau_chemin)
        self.barre_chemin.chemin_actuel.set(nouveau_chemin)

    def mettre_a_jour_barre(self, nouveau_chemin):
        # Remplacer les \ par des /
        nouveau_chemin = nouveau_chemin.replace("\\", "/")
        self.barre_chemin.chemin_actuel.set(nouveau_chemin)

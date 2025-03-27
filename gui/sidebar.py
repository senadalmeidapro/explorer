import customtkinter as ctk
from pathlib import Path

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, affichage, **kwargs):
        super().__init__(master, bg_color="white", width=200, corner_radius=0, **kwargs)
        self.affichage = affichage
        self.create_widgets()

    def create_widgets(self):
        # Style général des boutons
        self.button_style = {
            "fg_color": "lightgrey",
            "corner_radius": 0,
            "text_color": "black",
            "hover_color": "#d3d3d3"  # Couleur au survol 
        }

        # Création des boutons avec texte aligné à gauche
        self.btn_recents = self.create_sticky_button("📁 Recents", self.afficher_recents)
        self.btn_favorites = self.create_sticky_button("⭐ Favorites", self.afficher_favorites)
        self.btn_computer = self.create_sticky_button("💻 Computer", self.afficher_computer)
        self.btn_bureau = self.create_sticky_button("📂 Bureau", self.afficher_bureau)
        self.btn_telechargements = self.create_sticky_button("⬇️ Téléchargements", self.afficher_telechargements)
        self.btn_documents = self.create_sticky_button("📄 Documents", self.afficher_documents)
        self.btn_photos = self.create_sticky_button("🌄 Photos", self.afficher_photos)
        self.btn_videos = self.create_sticky_button("🎥 Videos", self.afficher_videos)
        self.btn_audios = self.create_sticky_button("🎵 Audios", self.afficher_audios)

    def create_sticky_button(self, text, command):
        """Crée un bouton avec un effet sticky au survol et au clic, et un texte aligné à gauche."""
        btn = ctk.CTkButton(self, text=text, **self.button_style, command=command, anchor="w")  # Texte à gauche
        btn.pack(fill="x", padx=10, pady=5)

        # Ajout des effets sticky
        btn.bind("<Enter>", lambda e: btn.configure(fg_color="#bfbfbf"))  # Survol
        btn.bind("<Leave>", lambda e: btn.configure(fg_color="lightgrey"))  # Quitte le survol
        btn.bind("<ButtonPress-1>", lambda e: btn.configure(fg_color="#a9a9a9"))  # Clic
        btn.bind("<ButtonRelease-1>", lambda e: btn.configure(fg_color="#bfbfbf"))  # Relâche le clic

        return btn

    def afficher_recents(self):
        self.affichage.afficher_recents()

    def afficher_favorites(self):
        self.affichage.afficher_favoris()

    def afficher_computer(self):
        self.affichage.ouvrir_dossiernavc("C:/")

    def afficher_bureau(self):
        chemin = Path.home() / "Desktop"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))
    
    def afficher_telechargements(self):
        chemin = Path.home() / "Downloads"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))

    def afficher_documents(self):
        chemin = Path.home() / "Documents"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))

    def afficher_photos(self):
        chemin = Path.home() / "Pictures"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))

    def afficher_videos(self):
        chemin = Path.home() / "Videos"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))

    def afficher_audios(self):
        chemin = Path.home() / "Music"
        if chemin.exists():
            self.affichage.ouvrir_dossiernavc(str(chemin))

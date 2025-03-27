import customtkinter as ctk
import tkinter as tk
from gui.affichage_fichiers import AffichageFichiers
from gestion.favoris import parcours
from threading import Thread

class BarreChemin(ctk.CTkFrame):
    def __init__(self, master, affichage, **kwargs):  # Ajout du paramètre affichage
        """
        :param master: le widget parent
        :param affichage: instance d'AffichageFichiers qui gère l'affichage et possède l'attribut 'chemin'
        """
        super().__init__(master, bg_color="white", height=40, **kwargs)
        self.affichage = affichage  # Maintenant, c'est une instance !
        self.chemin_actuel = tk.StringVar(value="C:/Users/senad/Documents")
        self.on_change = None  # Callback défini par le parent pour valider le changement de chemin
        self.create_widgets()
        self.grid_columnconfigure(4, weight=1)  # La colonne 4 (entrée) prend toute la largeur restante

    # Configure les colonnes et les lignes
        self.grid_columnconfigure(0, weight=0)  # Colonne des boutons
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=4)  # Colonne avec les entrées (qui doit prendre toute la largeur)
        self.grid_columnconfigure(5, weight=1)
        
        self.grid_rowconfigure(0, weight=1)  # Première ligne (contenant les boutons)
        self.grid_rowconfigure(1, weight=0)  # Deuxième ligne (contenant le frame)

    def create_widgets(self):
        self.plus = ctk.CTkButton(self, text="➕", width=4)
        self.prev = ctk.CTkButton(self, text="👈", width=4)
        self.next = ctk.CTkButton(self, text="👉", width=4)
        self.fresh = ctk.CTkButton(self, text="🔄", width=4)
        self.entry = ctk.CTkEntry(self, textvariable=self.chemin_actuel)
        self.entry1 = ctk.CTkEntry(self, placeholder_text="Rechercher un fichier ou dossier", placeholder_text_color="gray")
        
        # Placer les widgets dans la première ligne (row=0)
        self.plus.grid(row=0, column=0, padx=3, sticky="nsew")
        self.prev.grid(row=0, column=1, padx=3, sticky="nsew")
        self.next.grid(row=0, column=2, padx=3, sticky="nsew")
        self.fresh.grid(row=0, column=3, padx=3, sticky="nsew")
        self.entry.grid(row=0, column=4, padx=3, sticky="ew")
        self.entry1.grid(row=0, column=5, padx=3, sticky="ew")
        
        # Placer le frame dans la deuxième ligne (row=1)
        self.frame = ctk.CTkFrame(self, height=30)
        self.frame.grid(row=1, column=0, columnspan=6, padx=3, pady=6, sticky="ew", ipadx=6)  # Le frame prend toute la largeur
        
        # Configuration des colonnes pour permettre l'expansion dynamique
        for i in range(6):  # Il y a 9 éléments dans la ligne du frame
            self.frame.grid_columnconfigure(i, weight=0)  # Permet d'occuper tout l'espace disponible
        self.frame.grid_columnconfigure(6, weight=2)
        self.frame.grid_columnconfigure(7, weight=4)
        
        # Configuration de la ligne pour que les boutons puissent s'agrandir verticalement
        self.frame.grid_rowconfigure(0, weight=1)
        op=[
            "Tous",         # Afficher tous les fichiers et dossiers
            "Fichier",      # Afficher uniquement les fichiers
            "Dossier",      # Afficher uniquement les dossiers
            "Image",        # Afficher uniquement les fichiers image
            "Video",        # Afficher uniquement les fichiers vidéo
            "Audio",        # Afficher uniquement les fichiers audio
            "Fichier text", # Afficher uniquement les fichiers texte (.txt)
            "Autre"         # Afficher les fichiers qui ne sont ni images, vidéos, audios, ni texte
        ]
        
        self.btn1= ctk.CTkButton(self.frame, text="📂",width=50, fg_color="gray")
        self.btn2= ctk.CTkButton(self.frame, text="📄",width=50, fg_color="gray")
        self.btn3= ctk.CTkButton(self.frame, text="✂️",width=50, fg_color="gray")
        self.btn4= ctk.CTkButton(self.frame, text="📋",width=50, fg_color="gray")
        self.btn5= ctk.CTkButton(self.frame, text="🗑️",width=50, fg_color="gray")
        self.btn8= ctk.CTkButton(self.frame, text="🗑️Rennomer",width=50, fg_color="gray")
        self.btn6= ctk.CTkLabel(self.frame, text="Trier par")
        self.btn7= ctk.CTkComboBox(self.frame, values=op, command= self.on_combobox_select)
        self.btn1.grid(row=0 ,column=0,padx=1)
        self.btn2.grid(row=0 ,column=1,padx=1)
        self.btn3.grid(row=0 ,column=2,padx=1)
        self.btn4.grid(row=0 ,column=3,padx=1)
        self.btn5.grid(row=0 ,column=4,padx=1)
        self.btn6.grid(row=0 ,column=9,padx=3)
        self.btn7.grid(row=0 ,column=10,padx=3)
        


        # Lier l'événement <<ComboboxSelected>> à la fonction
        
        self.plus.bind("<ButtonRelease-1>", self.func_plus)
        self.prev.bind("<ButtonRelease-1>", self.func_prev)
        self.next.bind("<ButtonRelease-1>", self.func_next)
        self.fresh.bind("<ButtonRelease-1>", self.func_fresh)
        self.entry.bind("<Return>", self.valider_chemin)
        self.entry1.bind("<Return>", self.search)
        self.btn1.bind("<ButtonRelease-1>", self.new)
        self.btn2.bind("<ButtonRelease-1>", self.copi)
        self.btn3.bind("<ButtonRelease-1>", self.coup)
        self.btn4.bind("<ButtonRelease-1>", self.coll)
        self.btn5.bind("<ButtonRelease-1>", self.sup)

    def valider_chemin(self, event):
        nouveau_chemin = self.chemin_actuel.get()
        if self.on_change:
            self.on_change(nouveau_chemin)
    
    def search(self, event):
        term = self.entry1.get().strip()
        # Appelle la méthode presearche sur l'instance d'affichage
        # Créer et démarrer un thread pour appeler la fonction presearche
        search_thread = Thread(target=self.affichage.presearche, args=(term,))
        search_thread.start()
    
    def copi(self, event=None):
        self.affichage.cop_el()
        
    
    def coup(self, event=None):
        self.affichage.coup_el()
        
    
    def coll(self, event=None):
        self.affichage.col_el()
        
    
    def new(self, event=None):
        self.affichage.add_el()
        
    
    def sup(self, event=None):
        self.affichage.sup_el()
        
    
    def on_combobox_select(self, event=None):
        # Récupérer la valeur sélectionnée
        selected_value = self.btn7.get().strip()
        
        # Créer un thread pour exécuter le tri et l'affichage en arrière-plan
        Thread(target=self.affichage.trier_et_afficher, args=(selected_value.lower(),)).start()
        
    def func_plus(self, event):
        self.menu = tk.Menu(self.plus, tearoff=0)
        self.menu.add_command(label="Précédent", command=self.func_prev)
        self.menu.add_command(label="Suivant", command=self.func_next)
        self.menu.add_command(label="Actualiser", command=self.func_fresh_menu)
        self.menu.add_command(label="Nouveau dossier")
        self.menu.add_command(label="Nouveau fichier")
        self.menu.post(event.x_root, event.y_root)


    def func_prev(self, event=None):
        """Navigation vers le chemin précédent."""
        chemin_prev, existe = parcours("prev")
        if existe and chemin_prev:  # Vérifie si un chemin précédent existe
            self.affichage.ouvrir_dossiernav(chemin_prev)  # Ouvre le chemin précédent
            self.update_navigation_buttons()  # Met à jour l'état des boutons

    def func_next(self, event=None):
        """Navigation vers le chemin suivant."""
        chemin_next, existe = parcours("next")
        if existe and chemin_next:  # Vérifie si un chemin suivant existe
            self.affichage.ouvrir_dossiernav(chemin_next)  # Ouvre le chemin suivant
            self.update_navigation_buttons()  # Met à jour l'état des boutons

    def update_navigation_buttons(self):
        """Met à jour l'état des boutons Précédent et Suivant."""
        chemin_prev, existe_prev = parcours("prev")
        chemin_next, existe_next = parcours("nexts")

        # Désactive le bouton "Précédent" si on est au début
        self.prev.configure(state="disabled" if not existe_prev else "normal")

        # Désactive le bouton "Suivant" si on est à la fin
        self.next.configure(state="disabled" if not existe_next else "normal")



    def func_fresh(self, event):
        self.affichage.rafraichir_affichage()
        
    def func_fresh_menu(self):
        self.affichage.rafraichir_affichage()

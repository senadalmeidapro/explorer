import tkinter as tk
from tkinter import ttk
from gui.menus_contextuels import MenusContextuels
from gestion.navigation import lister_repertoire
from gestion.favoris import add_recents, lister_favoris, send_recent
from gestion.operations_fichiers import creer_dossier, supprimer_element, custom_show_error, copier_element, couper_element, coller_element, renommer_element
import os
import time

def nettoyer_nom(nom):
    """Nettoie le nom en retirant les emojis et les espaces superflus."""
    return nom.lstrip("📁📄 ").strip()

class AffichageFichiers(tk.Frame):
    def __init__(self, master, chemin=None, update_barre_callback=None, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.chemin = chemin  # Répertoire de base
        self.update_barre_callback = update_barre_callback
        self.menus_contextuels = None
        self.ordre_croissant = True  # Initialisation de l'option de tri croissant
        self.create_widgets()
        self.afficher_contenu()
        self.contenu = None

    def create_widgets(self):
        # Création d'une barre de défilement verticale
        self.scrollbar = tk.Scrollbar(self, orient="vertical")
        
        # Ajout de la barre de défilement au Treeview
        self.tree = ttk.Treeview(self, columns=("Type", "Taille", "Date de création"), show="tree headings", yscrollcommand=self.scrollbar.set)
        
        # Configuration de la barre de défilement
        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Ajouter du padding externe autour du Treeview
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Configuration de la police du Treeview (plus grande)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 13))  # Augmenter la taille de la police à 12 pour les éléments
        
        # Configuration des colonnes
        self.tree.heading("#0", text="Nom", command=lambda: self.trier_par_colonne("Nom"))
        self.tree.heading("Type", text="Type", command=lambda: self.trier_par_colonne("Type"))
        self.tree.heading("Taille", text="Taille", command=lambda: self.trier_par_colonne("Taille"))
        self.tree.heading("Date de création", text="Date de création", command=lambda: self.trier_par_colonne("Date de création"))
        
        # Largeur des colonnes (ajustée pour les rendre plus petites sauf la colonne "Nom")
        self.tree.column("#0", width=300, anchor="w")  # "Nom" colonne plus large
        
        # Ajustement automatique de la largeur des autres colonnes en fonction de la longueur du texte
        self.tree.column("Type", width=50, anchor="center")
        self.tree.column("Taille", width=50, anchor="center")
        self.tree.column("Date de création", width=10, anchor="center")
        
        # Appliquer la couleur bleue aux dossiers
        self.tree.tag_configure("dossier", foreground="blue")
        
        # Configuration automatique de la largeur des colonnes en fonction du contenu
        for col in ["Type", "Taille", "Date de création"]:
            max_len = 0
            for child in self.tree.get_children():
                text = self.tree.item(child, "values")[["Type", "Taille", "Date de création"].index(col)]
                max_len = max(max_len, len(str(text)))
            self.tree.column(col, width=max_len * 10)  # Ajuste la largeur de la colonne en fonction du texte le plus long

        self.tree.bind("<ButtonRelease-3>", self.afficher_menu_contextuel)
        self.tree.bind("<Double-1>", self.ouvrir_dossier)  # Bind pour double-clic

    def afficher_contenu(self):
        """Affiche le contenu du répertoire dans le Treeview."""
        # Vider le Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lister le contenu du répertoire
        self.contenu = lister_repertoire(self.chemin)
        if self.contenu:
            for element in self.contenu:
                # Vérifier que la clé 'date_creation' existe
                date_creation = element.get("date_creation", "Inconnu")
                # Appliquer le nettoyage sur le nom
                nom_nettoye = nettoyer_nom(element["nom"])
                # Si l'élément est un dossier, appliquer le tag "dossier"
                if element["type"] == "Dossier":
                    self.tree.insert("", "end", text=f"📁 {nom_nettoye}", values=(element["type"], element["taille"], date_creation), tags=("dossier",))
                else:
                    self.tree.insert("", "end",  text=f"📄 {nom_nettoye}", values=(element["type"], element["taille"], date_creation))
        else:
            pass

    def rafraichir_affichage(self):
        """Rafraîchit l'affichage du contenu du répertoire."""
        self.afficher_contenu()

    def afficher_menu_contextuel(self, event):
        """Affiche le menu contextuel lors d'un clic droit."""
        print("Clic droit détecté !")
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            print("Aucun élément sélectionné")
            return
        valeurs = self.tree.item(item_id, "values")
        if not valeurs:
            print("L'élément sélectionné n'a pas de valeurs associées")
            return
        type_element = valeurs[0]
        if type_element.lower().strip() not in ("dossier", "fichier"):
            print("Type non reconnu :", type_element)
            return
        nom_element = self.tree.item(item_id, "text")
        nom_element = nettoyer_nom(nom_element)
        chemin_acces = os.path.join(self.chemin, nom_element)
        # Instanciation du menu contextuel en passant self et le callback pour mettre à jour la barre d'adresse
        self.menus_contextuels = MenusContextuels(self.tree,
                                                 chemin_acces,
                                                 self.rafraichir_affichage,
                                                 self,
                                                 self.update_barre_callback)
        try:
            self.menus_contextuels.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menus_contextuels.menu.grab_release()

    def ouvrir_dossier(self, event):
        """Ouvre un dossier sélectionné dans l'application."""
        item_ids = self.tree.selection()
        if not item_ids:
            print("Aucun élément sélectionné")
            return

        # Utilisation du premier identifiant sélectionné
        item_id = item_ids[0]
        nom_element = self.tree.item(item_id, "text")
        nom_element = nettoyer_nom(nom_element)
        nouveau_chemin = os.path.join(self.chemin, nom_element)

        if os.path.isdir(nouveau_chemin):
            self.chemin = nouveau_chemin

            # Mise à jour de la barre d'adresse et ajout à l'historique
            if self.update_barre_callback:
                self.update_barre_callback(self.chemin)
                add_recents(self.chemin)

            # Mise à jour de l'affichage
            self.afficher_contenu()

    def ouvrir_dossiernavc(self, nouveau_chemin):
        """Ouvre un dossier sélectionné dans l'application par navigation."""
        if os.path.isdir(nouveau_chemin):
            self.chemin = nouveau_chemin

            # Mise à jour de l'historique et de la barre d'adresse
            if self.update_barre_callback:
                self.update_barre_callback(self.chemin)  # Met à jour la barre de navigation
                add_recents(self.chemin)

            # Mise à jour de l'affichage
            self.afficher_contenu()
    
    def ouvrir_dossiernav(self, nouveau_chemin):
        """Ouvre un dossier sélectionné dans l'application par navigation."""
        if os.path.isdir(nouveau_chemin):
            self.chemin = nouveau_chemin

            # Mise à jour de l'historique et de la barre d'adresse
            if self.update_barre_callback:
                self.update_barre_callback(self.chemin)  # Met à jour la barre de navigation

            # Mise à jour de l'affichage
            self.afficher_contenu()

    def presearche(self, terme):
        """Recherche un fichier ou un dossier dans le répertoire courant et ses sous-répertoires."""
        resultats = []
        # Parcours récursif du répertoire courant
        for root, dirs, files in os.walk(self.chemin):
            # Recherche dans les dossiers
            for dossier in dirs:
                if terme.lower() in dossier.lower():
                    resultats.append(os.path.join(root, dossier))
            # Recherche dans les fichiers
            for fichier in files:
                if terme.lower() in fichier.lower():
                    resultats.append(os.path.join(root, fichier))

        # Affichage des résultats dans le Treeview
        self.tree.delete(*self.tree.get_children())
        for chemin_resultat in resultats:
            nom = os.path.basename(chemin_resultat)
            if os.path.isdir(chemin_resultat):
                type_elem = "Dossier"
                taille = ""
            else:
                type_elem = "Fichier"
                try:
                    taille = os.path.getsize(chemin_resultat)
                except Exception as e:
                    taille = "Inconnu"
            self.tree.insert("", "end", text=nom, values=(type_elem, taille))
        return resultats

    def afficher_favoris(self):
        """Affiche la liste des favoris dans le Treeview."""
        favoris = lister_favoris()
        self.tree.delete(*self.tree.get_children())  # Effacer les éléments existants
        if favoris:
            for chemin_favori in favoris:
                nom_favori = os.path.basename(chemin_favori)
                nom_favori = nettoyer_nom(nom_favori)
                if os.path.isdir(chemin_favori):
                    type_elem = "Dossier"
                    taille = ""
                else:
                    type_elem = "Fichier"
                    try:
                        taille = os.path.getsize(chemin_favori)
                    except Exception as e:
                        taille = "Inconnu"
                self.tree.insert("", "end", text=nom_favori, values=(type_elem, taille))
        else:
            print("Aucun favori trouvé")
    
    def trier_et_afficher(self, filtre="tous"):
        """Trie le contenu du répertoire selon le filtre et met à jour l'affichage dans le Treeview."""
        self.tree.delete(*self.tree.get_children())  # Effacer l'affichage actuel

        extensions_images = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
        extensions_videos = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"}
        extensions_audios = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}

        contenu_filtre = []

        # Correction : appeler lister_repertoire directement, pas self.lister_repertoire
        contenu = lister_repertoire(self.chemin)
        for item in contenu:
            nom = item["nom"]
            type_element = item["type"]
            extension = os.path.splitext(nom)[1].lower() if type_element == "Fichier" else ""
            
            if filtre == "tous":
                contenu_filtre.append(item)
            elif filtre == "fichier" and type_element == "Fichier":
                contenu_filtre.append(item)
            elif filtre == "dossier" and type_element == "Dossier":
                contenu_filtre.append(item)
            elif filtre == "image" and extension in extensions_images:
                contenu_filtre.append(item)
            elif filtre == "video" and extension in extensions_videos:
                contenu_filtre.append(item)
            elif filtre == "audio" and extension in extensions_audios:
                contenu_filtre.append(item)
            elif filtre == "fichier text" and type_element == "Fichier" and extension == ".txt":
                contenu_filtre.append(item)
            elif filtre == "autre" and type_element == "Fichier" and extension not in (extensions_images | extensions_videos | extensions_audios | {".txt"}):
                contenu_filtre.append(item)

        # Mise à jour du Treeview avec le contenu filtré
        for element in contenu_filtre:
            tags = ("dossier",) if element["type"] == "Dossier" else ()
            date_creation = element.get("date_creation", "Inconnu")
            nom_nettoye = nettoyer_nom(element["nom"])
            self.tree.insert("", "end", text=nom_nettoye, values=(element["type"], element["taille"], date_creation), tags=tags)

    def trier_par_colonne(self, colonne):
        elements = [(self.tree.item(item_id, "text"), self.tree.item(item_id, "values"), item_id)
                    for item_id in self.tree.get_children()]
        
        index_colonne = {"Nom": 0, "Type": 1, "Taille": 2, "Date de création": 3}.get(colonne, 0)

        def convert_taille(val):
            try:
                return int(val.split()[0])
            except:
                return 0

        def convertir_date(val):
            try:
                return time.mktime(time.strptime(val, "%Y-%m-%d %H:%M:%S"))
            except:
                return 0

        if index_colonne == 0:
            key_func = lambda elem: elem[0].lower()
        elif index_colonne == 1:
            key_func = lambda elem: elem[1][0] if elem[1] else ""
        elif index_colonne == 2:
            key_func = lambda elem: convert_taille(elem[1][1]) if len(elem[1]) > 1 else 0
        elif index_colonne == 3:
            key_func = lambda elem: convertir_date(elem[1][2]) if len(elem[1]) > 2 else 0
        else:
            key_func = lambda elem: elem[0].lower()

        elements.sort(key=key_func, reverse=not self.ordre_croissant)
        self.ordre_croissant = not self.ordre_croissant

        self.tree.delete(*self.tree.get_children())
        for nom, valeurs, _ in elements:
            tags = ("dossier",) if valeurs and valeurs[0] == "Dossier" else ()
            self.tree.insert("", "end", text=nom, values=valeurs, tags=tags)
    
    def get_chemin_selectionne(self):
        """Récupère le chemin complet de l'élément sélectionné dans le Treeview."""
        # Récupérer l'ID de l'élément sélectionné
        item_ids = self.tree.selection()
        if not item_ids:
            return None
        # Récupérer le nom (texte) de l'élément sélectionné et le nettoyer
        nom_element = self.tree.item(item_ids[0], "text")
        nom_element = nom_element.lstrip("📁📄 ").strip()
        chemin_complet = os.path.join(self.chemin, nom_element)
        return chemin_complet
        
    def add_el(self):
        # Appelle creer_dossier avec le répertoire courant et le callback de mise à jour
        creer_dossier(self.chemin, update_barre_callback=self.update_barre_callback)
        # Rafraîchir l'affichage après création
        self.afficher_contenu()

    def sup_el(self):
        chemin_selectionne = self.get_chemin_selectionne()
        if not chemin_selectionne:
            custom_show_error("Erreur", "Aucun élément à supprimer.")
            return
        # Extraire le nom de l'élément depuis son chemin
        nom = os.path.basename(chemin_selectionne)
        # Appel de la fonction supprimer_element avec le nom et le répertoire courant
        supprimer_element(nom, self.chemin)
        # Rafraîchir l'affichage après suppression
        self.afficher_contenu()
    
    def ren_el(self):
        chemin_selectionne = self.get_chemin_selectionne()
        if not chemin_selectionne:
            custom_show_error("Erreur", "Aucun élément à renomer.")
            return
        # Extraire le nom de l'élément depuis son chemin
        nom = os.path.basename(chemin_selectionne)
        # Appel de la fonction renommer_element avec le nom et le répertoire courant
        renommer_element(nom, self.chemin)
        # Rafraîchir l'affichage après suppression
        self.afficher_contenu()
        
    def cop_el(self):
        chemin_selectionne = self.get_chemin_selectionne()
        if not chemin_selectionne:
            custom_show_error("Erreur", "Aucun élément à copier.")
            return
        # Extraire le nom de l'élément depuis son chemin
        nom = os.path.basename(chemin_selectionne)
        # Appel de la fonction copier_element avec le nom et le répertoire courant
        copier_element(nom, self.chemin)
        # Rafraîchir l'affichage après suppression
        self.afficher_contenu()
    
    def coup_el(self):
        chemin_selectionne = self.get_chemin_selectionne()
        if not chemin_selectionne:
            custom_show_error("Erreur", "Aucun élément à ccouperoller.")
            return
        # Extraire le nom de l'élément depuis son chemin
        nom = os.path.basename(chemin_selectionne)
        # Appel de la fonction couper_element avec le nom et le répertoire courant
        couper_element(nom, self.chemin)
        # Rafraîchir l'affichage après suppression
        self.afficher_contenu()
    
    def col_el(self):
        coller_element()
        # Rafraîchir l'affichage après suppression
        self.afficher_contenu()

    def afficher_recents(self):
        # Récupère les fichiers récents, les traite et les passe à afficher_contenu pour affichage.
        # Effacer l'affichage actuel dans le Treeview
        self.tree.delete(*self.tree.get_children())

        # Récupérer la liste des chemins récents
        recents_list = send_recent()

        # Liste pour stocker les informations des fichiers traités
        fichiers_traite = []

        if recents_list:
            for chemin in recents_list:
                if os.path.exists(chemin):  # Vérifier si le fichier/dossier existe
                    nom = os.path.basename(chemin)
                    nom = nom.lstrip("📁📄 ").strip()

                    # Déterminer le type (dossier ou fichier) et récupérer la taille
                    if os.path.isdir(chemin):
                        type_elem = "Dossier"
                        taille = ""  # Pas de taille pour les dossiers
                    else:
                        type_elem = "Fichier"
                        try:
                            taille_val = os.path.getsize(chemin)
                            taille = f"{taille_val} octets"
                        except Exception:
                            taille = "Inconnu"
                    
                    # Récupérer la date de modification (modification et création ont des comportements similaires)
                    try:
                        date_modification = os.path.getmtime(chemin)
                        date_modification = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(date_modification))
                    except Exception:
                        date_modification = "Inconnu"
                    
                    # Ajouter les informations traitées à la liste
                    fichiers_traite.append({
                        "nom": nom,
                        "type": type_elem,
                        "taille": taille,
                        "date_creation": date_modification  # Utiliser la date de modification pour "date_creation"
                    })
            
            # Transmettre la liste traitée à afficher_contenu pour affichage
            self.contenu = fichiers_traite
            self.afficher_contenu()
        else:
            print("Aucun fichier récent trouvé")
